"""
Switch App File Manager - Comprehensive file upload and storage management
Handles file uploads, Cloud Storage, Firebase integration, and file organization
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List
from google.cloud import firestore, storage
from google.adk.tools import ToolContext

PROJECT_ID = "studio-2416451423-f2d96"
STORAGE_BUCKET = f"{PROJECT_ID}.appspot.com"

db = firestore.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)


def upload_file_to_storage(
    file_content: str,
    file_name: str,
    user_id: str,
    file_type: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Upload a file to Cloud Storage and save metadata to Firestore.
    
    Args:
        file_content: Base64 encoded file content or file path
        file_name: Name of the file
        user_id: ID of the user uploading the file
        file_type: Type of file (image, video, document, audio, etc.)
        
    Returns:
        dict: Upload result with file URL and metadata
    """
    try:
        import base64
        
        # Decode base64 if needed
        if file_content.startswith('data:'):
            # Extract base64 data from data URL
            file_content = file_content.split(',')[1]
        
        try:
            file_bytes = base64.b64decode(file_content)
        except:
            # If not base64, treat as file path
            with open(file_content, 'rb') as f:
                file_bytes = f.read()
        
        # Generate unique file path
        file_hash = hashlib.md5(file_bytes).hexdigest()[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        storage_path = f"users/{user_id}/files/{timestamp}_{file_hash}_{file_name}"
        
        # Upload to Cloud Storage
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(storage_path)
        
        # Set content type
        content_types = {
            'image': 'image/jpeg',
            'video': 'video/mp4',
            'document': 'application/pdf',
            'audio': 'audio/mpeg'
        }
        blob.content_type = content_types.get(file_type, 'application/octet-stream')
        
        # Upload
        blob.upload_from_string(file_bytes)
        
        # Make publicly accessible (or use signed URLs for private)
        # blob.make_public()
        # public_url = blob.public_url
        
        # Generate signed URL (valid for 7 days)
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=7),
            method="GET"
        )
        
        # Save metadata to Firestore
        file_metadata = {
            'file_id': f"{timestamp}_{file_hash}",
            'file_name': file_name,
            'file_type': file_type,
            'user_id': user_id,
            'storage_path': storage_path,
            'file_url': signed_url,
            'file_size': len(file_bytes),
            'uploaded_at': firestore.SERVER_TIMESTAMP,
            'status': 'active'
        }
        
        doc_ref = db.collection('switch_app_files').document(file_metadata['file_id'])
        doc_ref.set(file_metadata)
        
        return {
            'status': 'success',
            'file_id': file_metadata['file_id'],
            'file_name': file_name,
            'file_url': signed_url,
            'file_type': file_type,
            'file_size': len(file_bytes),
            'storage_path': storage_path,
            'message': 'File uploaded successfully'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to upload file: {str(e)}'
        }


def process_image_file(
    file_id: str,
    analysis_type: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Process an image file using Vision API.
    
    Args:
        file_id: ID of the uploaded file
        analysis_type: Type of analysis (labels, text, faces, objects, etc.)
        
    Returns:
        dict: Analysis results
    """
    try:
        from google.cloud import vision
        
        # Get file metadata
        doc_ref = db.collection('switch_app_files').document(file_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return {
                'status': 'error',
                'message': 'File not found'
            }
        
        file_data = doc.to_dict()
        storage_path = file_data['storage_path']
        
        # Get file from storage
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(storage_path)
        image_bytes = blob.download_as_bytes()
        
        # Analyze with Vision API
        vision_client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        
        results = {}
        
        if analysis_type == 'labels' or analysis_type == 'all':
            response = vision_client.label_detection(image=image)
            results['labels'] = [
                {'description': label.description, 'score': label.score}
                for label in response.label_annotations
            ]
        
        if analysis_type == 'text' or analysis_type == 'all':
            response = vision_client.text_detection(image=image)
            if response.text_annotations:
                results['text'] = response.text_annotations[0].description
        
        if analysis_type == 'objects' or analysis_type == 'all':
            response = vision_client.object_localization(image=image)
            results['objects'] = [
                {'name': obj.name, 'score': obj.score}
                for obj in response.localized_object_annotations
            ]
        
        # Save analysis results
        doc_ref.update({
            'analysis_results': results,
            'analyzed_at': firestore.SERVER_TIMESTAMP
        })
        
        return {
            'status': 'success',
            'file_id': file_id,
            'analysis_type': analysis_type,
            'results': results,
            'message': 'Image processed successfully'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to process image: {str(e)}'
        }


def get_user_files(
    user_id: str,
    file_type: str,
    limit: int,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Get all files for a user.
    
    Args:
        user_id: ID of the user
        file_type: Filter by file type (all, image, video, document, audio)
        limit: Maximum number of files to return
        
    Returns:
        dict: List of user files
    """
    try:
        query = db.collection('switch_app_files').where('user_id', '==', user_id)
        
        if file_type != 'all':
            query = query.where('file_type', '==', file_type)
        
        query = query.order_by('uploaded_at', direction=firestore.Query.DESCENDING).limit(limit)
        
        files = []
        for doc in query.stream():
            file_data = doc.to_dict()
            files.append({
                'file_id': file_data['file_id'],
                'file_name': file_data['file_name'],
                'file_type': file_data['file_type'],
                'file_url': file_data['file_url'],
                'file_size': file_data['file_size'],
                'uploaded_at': file_data.get('uploaded_at'),
                'has_analysis': 'analysis_results' in file_data
            })
        
        return {
            'status': 'success',
            'user_id': user_id,
            'file_count': len(files),
            'files': files,
            'message': f'Found {len(files)} files'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to get files: {str(e)}'
        }


def delete_file(
    file_id: str,
    user_id: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Delete a file from storage and Firestore.
    
    Args:
        file_id: ID of the file to delete
        user_id: ID of the user (for verification)
        
    Returns:
        dict: Deletion result
    """
    try:
        # Get file metadata
        doc_ref = db.collection('switch_app_files').document(file_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return {
                'status': 'error',
                'message': 'File not found'
            }
        
        file_data = doc.to_dict()
        
        # Verify ownership
        if file_data['user_id'] != user_id:
            return {
                'status': 'error',
                'message': 'Permission denied'
            }
        
        # Delete from Cloud Storage
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(file_data['storage_path'])
        blob.delete()
        
        # Delete from Firestore
        doc_ref.delete()
        
        return {
            'status': 'success',
            'file_id': file_id,
            'file_name': file_data['file_name'],
            'message': 'File deleted successfully'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to delete file: {str(e)}'
        }


def generate_signed_url(
    file_id: str,
    expiration_hours: int,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Generate a new signed URL for a file.
    
    Args:
        file_id: ID of the file
        expiration_hours: Hours until URL expires
        
    Returns:
        dict: New signed URL
    """
    try:
        # Get file metadata
        doc_ref = db.collection('switch_app_files').document(file_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return {
                'status': 'error',
                'message': 'File not found'
            }
        
        file_data = doc.to_dict()
        storage_path = file_data['storage_path']
        
        # Generate new signed URL
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(storage_path)
        
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(hours=expiration_hours),
            method="GET"
        )
        
        # Update Firestore
        doc_ref.update({
            'file_url': signed_url,
            'url_updated_at': firestore.SERVER_TIMESTAMP
        })
        
        return {
            'status': 'success',
            'file_id': file_id,
            'file_url': signed_url,
            'expires_in_hours': expiration_hours,
            'message': 'Signed URL generated'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to generate signed URL: {str(e)}'
        }


def create_file_collection(
    user_id: str,
    collection_name: str,
    file_ids: list,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Create a collection/album of files.
    
    Args:
        user_id: ID of the user
        collection_name: Name of the collection
        file_ids: List of file IDs to include
        
    Returns:
        dict: Collection details
    """
    try:
        # Verify all files belong to user
        for file_id in file_ids:
            doc_ref = db.collection('switch_app_files').document(file_id)
            doc = doc_ref.get()
            
            if not doc.exists or doc.to_dict()['user_id'] != user_id:
                return {
                    'status': 'error',
                    'message': f'Invalid file ID or permission denied: {file_id}'
                }
        
        # Create collection
        collection_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        collection_data = {
            'collection_id': collection_id,
            'user_id': user_id,
            'collection_name': collection_name,
            'file_ids': file_ids,
            'file_count': len(file_ids),
            'created_at': firestore.SERVER_TIMESTAMP,
            'status': 'active'
        }
        
        doc_ref = db.collection('switch_app_collections').document(collection_id)
        doc_ref.set(collection_data)
        
        return {
            'status': 'success',
            'collection_id': collection_id,
            'collection_name': collection_name,
            'file_count': len(file_ids),
            'message': 'Collection created successfully'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to create collection: {str(e)}'
        }


__all__ = [
    'upload_file_to_storage',
    'process_image_file',
    'get_user_files',
    'delete_file',
    'generate_signed_url',
    'create_file_collection'
]