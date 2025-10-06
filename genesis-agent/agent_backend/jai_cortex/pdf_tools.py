"""
PDF Tools - Generate and process PDFs in ADK
Based on ADK's medical-pre-authorization example
"""

import io
import base64
from typing import Dict, Any
from datetime import datetime
from google.cloud import storage, firestore
from google.adk.tools import ToolContext

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

PROJECT_ID = "studio-2416451423-f2d96"
STORAGE_BUCKET = f"{PROJECT_ID}.appspot.com"

db = firestore.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)


def generate_pdf_report(
    title: str,
    content: str,
    output_name: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Generate a PDF report from text content.
    
    Args:
        title: Title of the PDF
        content: Text content to include
        output_name: Name for the output file (without .pdf)
        
    Returns:
        dict: PDF generation result with download URL
    """
    if not REPORTLAB_AVAILABLE:
        return {
            'status': 'error',
            'message': 'ReportLab not installed. Add "reportlab>=4.4.3" to requirements.txt'
        }
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"{output_name}_{timestamp}.pdf"
        
        # Create PDF in memory
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title_style = styles['Title']
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.2 * letter[1]))
        
        # Add content paragraphs
        for paragraph_text in content.split('\n\n'):
            if paragraph_text.strip():
                p = Paragraph(paragraph_text.strip().replace('\n', '<br/>'), styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 0.05 * letter[1]))
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        
        # Upload to Cloud Storage
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(f'pdfs/{pdf_filename}')
        blob.upload_from_file(pdf_buffer, content_type='application/pdf')
        
        # Generate signed URL (valid for 7 days)
        from datetime import timedelta
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=7),
            method="GET"
        )
        
        # Save metadata to Firestore
        pdf_metadata = {
            'pdf_id': f'pdf_{timestamp}',
            'title': title,
            'filename': pdf_filename,
            'storage_path': f'pdfs/{pdf_filename}',
            'download_url': signed_url,
            'created_at': firestore.SERVER_TIMESTAMP,
            'size_bytes': len(pdf_buffer.getvalue())
        }
        
        db.collection('generated_pdfs').document(pdf_metadata['pdf_id']).set(pdf_metadata)
        
        pdf_buffer.close()
        
        return {
            'status': 'success',
            'pdf_id': pdf_metadata['pdf_id'],
            'filename': pdf_filename,
            'download_url': signed_url,
            'storage_path': f'gs://{STORAGE_BUCKET}/pdfs/{pdf_filename}',
            'size_bytes': pdf_metadata['size_bytes'],
            'message': f'PDF generated: {pdf_filename}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to generate PDF: {str(e)}'
        }


def extract_text_from_pdf(
    pdf_url: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_url: URL or GCS path to PDF file
        
    Returns:
        dict: Extracted text content
    """
    if not PDFPLUMBER_AVAILABLE:
        return {
            'status': 'error',
            'message': 'pdfplumber not installed. Add "pdfplumber>=0.11.7" to requirements.txt'
        }
    
    try:
        # Download PDF
        if pdf_url.startswith('gs://'):
            # GCS path
            path_parts = pdf_url.replace('gs://', '').split('/', 1)
            bucket_name = path_parts[0]
            blob_path = path_parts[1]
            
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            pdf_bytes = blob.download_as_bytes()
        else:
            # HTTP URL
            import requests
            response = requests.get(pdf_url)
            pdf_bytes = response.content
        
        # Extract text
        pdf_text = ""
        with io.BytesIO(pdf_bytes) as pdf_file:
            with pdfplumber.open(pdf_file) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        pdf_text += f"\n--- Page {page_num} ---\n{page_text}\n"
        
        return {
            'status': 'success',
            'pdf_url': pdf_url,
            'text_content': pdf_text,
            'page_count': len(pdf.pages) if 'pdf' in locals() else 0,
            'char_count': len(pdf_text),
            'message': 'Text extracted successfully'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to extract text from PDF: {str(e)}'
        }


def create_pdf_from_markdown(
    markdown_content: str,
    output_name: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Convert Markdown to PDF.
    
    Args:
        markdown_content: Markdown formatted text
        output_name: Name for the output file
        
    Returns:
        dict: PDF generation result
    """
    if not REPORTLAB_AVAILABLE:
        return {
            'status': 'error',
            'message': 'ReportLab not installed'
        }
    
    try:
        # Simple markdown to HTML conversion
        html_content = markdown_content
        
        # Convert markdown headers
        html_content = html_content.replace('# ', '<h1>').replace('\n', '</h1>\n')
        html_content = html_content.replace('## ', '<h2>').replace('\n', '</h2>\n')
        html_content = html_content.replace('### ', '<h3>').replace('\n', '</h3>\n')
        
        # Convert bold and italic
        html_content = html_content.replace('**', '<b>').replace('**', '</b>')
        html_content = html_content.replace('*', '<i>').replace('*', '</i>')
        
        # Convert lists
        lines = html_content.split('\n')
        in_list = False
        processed_lines = []
        
        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    processed_lines.append('<ul>')
                    in_list = True
                processed_lines.append(f'<li>{line.strip()[2:]}</li>')
            else:
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                processed_lines.append(line)
        
        if in_list:
            processed_lines.append('</ul>')
        
        html_content = '\n'.join(processed_lines)
        
        # Generate PDF from HTML
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"{output_name}_{timestamp}.pdf"
        
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add content
        for paragraph_text in html_content.split('\n\n'):
            if paragraph_text.strip():
                p = Paragraph(paragraph_text.strip(), styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 0.05 * letter[1]))
        
        doc.build(story)
        pdf_buffer.seek(0)
        
        # Upload to Cloud Storage
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(f'pdfs/{pdf_filename}')
        blob.upload_from_file(pdf_buffer, content_type='application/pdf')
        
        from datetime import timedelta
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=7),
            method="GET"
        )
        
        pdf_buffer.close()
        
        return {
            'status': 'success',
            'filename': pdf_filename,
            'download_url': signed_url,
            'message': 'Markdown converted to PDF'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to convert markdown to PDF: {str(e)}'
        }


def create_pdf_invoice(
    invoice_data: dict,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Generate a professional invoice PDF.
    
    Args:
        invoice_data: Invoice details (customer, items, amounts)
        
    Returns:
        dict: PDF generation result
    """
    if not REPORTLAB_AVAILABLE:
        return {
            'status': 'error',
            'message': 'ReportLab not installed'
        }
    
    try:
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import Table, TableStyle
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        invoice_number = invoice_data.get('invoice_number', f'INV-{timestamp}')
        pdf_filename = f"invoice_{invoice_number}.pdf"
        
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph(f"<b>INVOICE #{invoice_number}</b>", styles['Title']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Customer info
        customer = invoice_data.get('customer', {})
        story.append(Paragraph(f"<b>Bill To:</b>", styles['Heading2']))
        story.append(Paragraph(customer.get('name', 'N/A'), styles['Normal']))
        story.append(Paragraph(customer.get('address', ''), styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Invoice date
        invoice_date = invoice_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        story.append(Paragraph(f"<b>Date:</b> {invoice_date}", styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Items table
        items = invoice_data.get('items', [])
        table_data = [['Item', 'Quantity', 'Price', 'Total']]
        
        for item in items:
            table_data.append([
                item.get('description', ''),
                str(item.get('quantity', 0)),
                f"${item.get('price', 0):.2f}",
                f"${item.get('quantity', 0) * item.get('price', 0):.2f}"
            ])
        
        # Total
        total = sum(item.get('quantity', 0) * item.get('price', 0) for item in items)
        table_data.append(['', '', '<b>TOTAL:</b>', f"<b>${total:.2f}</b>"])
        
        table = Table(table_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5 * inch))
        
        # Payment terms
        story.append(Paragraph("<b>Payment Terms:</b> Due within 30 days", styles['Normal']))
        
        doc.build(story)
        pdf_buffer.seek(0)
        
        # Upload to Cloud Storage
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(f'invoices/{pdf_filename}')
        blob.upload_from_file(pdf_buffer, content_type='application/pdf')
        
        from datetime import timedelta
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=30),
            method="GET"
        )
        
        pdf_buffer.close()
        
        return {
            'status': 'success',
            'invoice_number': invoice_number,
            'filename': pdf_filename,
            'download_url': signed_url,
            'total_amount': total,
            'message': f'Invoice generated: {invoice_number}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to generate invoice: {str(e)}'
        }


__all__ = [
    'generate_pdf_report',
    'extract_text_from_pdf',
    'create_pdf_from_markdown',
    'create_pdf_invoice'
]
