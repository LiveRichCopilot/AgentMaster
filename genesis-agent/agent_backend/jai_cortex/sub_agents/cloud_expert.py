"""
CloudExpert - Google Cloud Platform Specialist with Real GCP Tools
Part of JAi Cortex OS Multi-Agent System
"""

import os
from typing import Optional
from google.adk.agents import Agent
from google.adk.tools import ToolContext, FunctionTool
from google.genai import types as genai_types
from google.cloud import storage, firestore, resourcemanager_v3, secretmanager
from google.cloud.service_usage_v1 import ServiceUsageClient
from google.cloud.service_usage_v1.types import ListServicesRequest
import google.auth
from google.api_core import exceptions as gcp_exceptions


# Get project ID from environment or credentials
try:
    credentials, project_id = google.auth.default()
    PROJECT_ID = project_id or os.environ.get('GOOGLE_CLOUD_PROJECT', 'studio-2416451423-f2d96')
except Exception:
    PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', 'studio-2416451423-f2d96')


def check_project_status(tool_context: ToolContext) -> dict:
    """Check Google Cloud project status and configuration.
    
    This tool retrieves information about the current GCP project including:
    - Project ID and name
    - Project state (active, deleted, etc.)
    - Project number
    - Basic project metadata
    
    Returns:
        dict: Project information including ID, name, state, and number
    """
    try:
        client = resourcemanager_v3.ProjectsClient()
        project_name = f"projects/{PROJECT_ID}"
        
        project = client.get_project(name=project_name)
        
        return {
            'status': 'success',
            'project_id': PROJECT_ID,
            'project_name': project.display_name,
            'project_number': project.name.split('/')[-1],
            'state': project.state.name,
            'message': f'Project {PROJECT_ID} is {project.state.name.lower()}'
        }
    except gcp_exceptions.PermissionDenied:
        return {
            'status': 'error',
            'message': f'Permission denied. Service account needs roles/resourcemanager.projectViewer role for project {PROJECT_ID}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error checking project status: {str(e)}'
        }


def list_enabled_services(tool_context: ToolContext) -> dict:
    """List all enabled Google Cloud services/APIs for the current project.
    
    This tool shows which GCP services are currently enabled, such as:
    - Vertex AI API
    - Cloud Run API
    - Firestore API
    - Cloud Storage API
    - etc.
    
    Returns:
        dict: List of enabled services with their names and states
    """
    try:
        client = ServiceUsageClient()
        parent = f"projects/{PROJECT_ID}"
        
        services = []
        request = ListServicesRequest(
            parent=parent,
            filter="state:ENABLED",
            page_size=100
        )
        
        for service in client.list_services(request=request):
            service_name = service.config.name.replace('.googleapis.com', '')
            services.append({
                'name': service_name,
                'full_name': service.config.name,
                'state': service.state.name
            })
        
        # Highlight key services
        key_services = ['aiplatform', 'run', 'firestore', 'storage', 'cloudfunctions']
        enabled_key_services = [s['name'] for s in services if any(key in s['name'] for key in key_services)]
        
        return {
            'status': 'success',
            'project_id': PROJECT_ID,
            'total_enabled': len(services),
            'key_services_enabled': enabled_key_services,
            'all_services': services[:20],  # Return first 20 to avoid too much data
            'message': f'Found {len(services)} enabled services in {PROJECT_ID}'
        }
    except gcp_exceptions.PermissionDenied:
        return {
            'status': 'error',
            'message': f'Permission denied. Service account needs roles/serviceusage.serviceUsageViewer role'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error listing services: {str(e)}'
        }


def check_cloud_storage_buckets(tool_context: ToolContext) -> dict:
    """List and check Cloud Storage buckets in the current project.
    
    This tool retrieves information about all Cloud Storage buckets:
    - Bucket names and locations
    - Storage class (Standard, Nearline, etc.)
    - Size and object count (approximate)
    - Public access settings
    
    Returns:
        dict: List of buckets with their configurations
    """
    try:
        client = storage.Client(project=PROJECT_ID)
        
        buckets_info = []
        for bucket in client.list_buckets():
            buckets_info.append({
                'name': bucket.name,
                'location': bucket.location,
                'storage_class': bucket.storage_class,
                'created': bucket.time_created.isoformat() if bucket.time_created else None,
                'public': bucket.iam_configuration.public_access_prevention == 'inherited'
            })
        
        return {
            'status': 'success',
            'project_id': PROJECT_ID,
            'total_buckets': len(buckets_info),
            'buckets': buckets_info,
            'message': f'Found {len(buckets_info)} Cloud Storage buckets'
        }
    except gcp_exceptions.PermissionDenied:
        return {
            'status': 'error',
            'message': 'Permission denied. Service account needs roles/storage.admin or roles/storage.objectViewer role'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error checking Cloud Storage: {str(e)}'
        }


def check_firestore_database(database_id: str = 'agent-master-database', tool_context: ToolContext = None) -> dict:
    """Check Firestore database status and collections.
    
    This tool retrieves information about Firestore databases:
    - Database existence and state
    - List of collections
    - Approximate document counts per collection
    
    Args:
        database_id: Firestore database ID (default: 'agent-master-database')
        
    Returns:
        dict: Database status and collection information
    """
    try:
        db = firestore.Client(project=PROJECT_ID, database=database_id)
        
        # List collections
        collections = []
        for collection_ref in db.collections():
            collection_name = collection_ref.id
            # Get approximate count (limited to first 100 for performance)
            docs = list(collection_ref.limit(100).stream())
            collections.append({
                'name': collection_name,
                'sample_doc_count': len(docs),
                'has_more': len(docs) == 100
            })
        
        return {
            'status': 'success',
            'project_id': PROJECT_ID,
            'database_id': database_id,
            'total_collections': len(collections),
            'collections': collections,
            'message': f'Firestore database "{database_id}" is accessible with {len(collections)} collections'
        }
    except gcp_exceptions.PermissionDenied:
        return {
            'status': 'error',
            'message': 'Permission denied. Service account needs roles/datastore.user role for Firestore access'
        }
    except gcp_exceptions.NotFound:
        return {
            'status': 'error',
            'message': f'Firestore database "{database_id}" not found in project {PROJECT_ID}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error checking Firestore: {str(e)}'
        }


def check_iam_permissions(service_account_email: str, tool_context: ToolContext) -> dict:
    """Check IAM permissions for a specific service account.
    
    This tool helps debug permission issues by checking what roles
    a service account has and suggesting missing permissions.
    
    Args:
        service_account_email: Service account email to check
        
    Returns:
        dict: List of roles and permission recommendations
    """
    try:
        # Common roles and their purposes
        common_roles = {
            'roles/aiplatform.user': 'Vertex AI access (required for Agent Engine)',
            'roles/storage.admin': 'Cloud Storage full access',
            'roles/datastore.user': 'Firestore read/write access',
            'roles/serviceusage.serviceUsageViewer': 'View enabled services',
            'roles/resourcemanager.projectViewer': 'View project information',
            'roles/run.admin': 'Cloud Run deployment and management',
            'roles/cloudfunctions.admin': 'Cloud Functions management'
        }
        
        return {
            'status': 'success',
            'service_account': service_account_email,
            'project_id': PROJECT_ID,
            'check_command': f'gcloud projects get-iam-policy {PROJECT_ID} --flatten="bindings[].members" --format="table(bindings.role)" --filter="bindings.members:{service_account_email}"',
            'recommended_roles': common_roles,
            'grant_command_template': f'gcloud projects add-iam-policy-binding {PROJECT_ID} --member="serviceAccount:{service_account_email}" --role="ROLE_NAME"',
            'message': f'Use the gcloud command above to check actual permissions for {service_account_email}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error preparing IAM check: {str(e)}'
        }


def create_firestore_database(database_id: str, location: str = "nam5", tool_context: ToolContext = None) -> dict:
    """Create a new Firestore database in the project.
    
    This tool provisions a NEW Firestore database. Use this when setting up a new application.
    
    Args:
        database_id: Name for the database (e.g., "switch-v2-db" or "(default)")
        location: Database location (default: "nam5" for North America multi-region)
        
    Returns:
        dict: Success status and database details
    """
    try:
        import subprocess
        
        # Use gcloud command to create database
        cmd = [
            "gcloud", "firestore", "databases", "create",
            f"--database={database_id}",
            f"--location={location}",
            f"--project={PROJECT_ID}",
            "--type=firestore-native"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return {
                'status': 'success',
                'database_id': database_id,
                'location': location,
                'project_id': PROJECT_ID,
                'message': f'Firestore database "{database_id}" created successfully in {location}'
            }
        else:
            error_msg = result.stderr or result.stdout
            return {
                'status': 'error',
                'message': f'Failed to create database: {error_msg}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error creating Firestore database: {str(e)}'
        }


def create_storage_bucket(bucket_name: str, location: str = "us-central1", tool_context: ToolContext = None) -> dict:
    """Create a new Cloud Storage bucket.
    
    This tool provisions a NEW storage bucket for files, videos, images, etc.
    
    Args:
        bucket_name: Globally unique bucket name (e.g., "switch-v2-assets")
        location: Bucket location (default: "us-central1")
        
    Returns:
        dict: Success status and bucket details
    """
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        
        bucket = storage_client.bucket(bucket_name)
        bucket.location = location
        bucket.storage_class = "STANDARD"
        
        new_bucket = storage_client.create_bucket(bucket, location=location)
        
        return {
            'status': 'success',
            'bucket_name': bucket_name,
            'location': location,
            'url': f'gs://{bucket_name}',
            'message': f'Storage bucket "{bucket_name}" created successfully'
        }
        
    except gcp_exceptions.Conflict:
        return {
            'status': 'error',
            'message': f'Bucket "{bucket_name}" already exists (bucket names must be globally unique)'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error creating storage bucket: {str(e)}'
        }


def write_file(file_path: str, content: str, tool_context: ToolContext = None) -> dict:
    """Write content to a file. Use this to create source code, configs, or Dockerfiles.
    
    Args:
        file_path: Path where to write the file (relative or absolute)
        content: The file content to write
        
    Returns:
        dict: Success status and file location
    """
    try:
        import os
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {
            'status': 'success',
            'file_path': file_path,
            'size': len(content),
            'message': f'File written successfully: {file_path}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error writing file: {str(e)}'
        }


def deploy_to_cloud_run(service_name: str, source_dir: str, region: str = "us-central1", 
                        env_vars: Optional[dict] = None, tool_context: ToolContext = None) -> dict:
    """Deploy an application to Cloud Run.
    
    This tool builds a container from source and deploys it to Cloud Run.
    
    Args:
        service_name: Name for the Cloud Run service
        source_dir: Directory containing the source code and Dockerfile
        region: Cloud Run region (default: "us-central1")
        env_vars: Optional environment variables as dict
        
    Returns:
        dict: Deployment status and service URL
    """
    try:
        import subprocess
        
        # Build the gcloud command
        cmd = [
            "gcloud", "run", "deploy", service_name,
            "--source", source_dir,
            "--region", region,
            "--platform", "managed",
            "--allow-unauthenticated",
            f"--project={PROJECT_ID}"
        ]
        
        # Add environment variables if provided
        if env_vars:
            env_str = ",".join([f"{k}={v}" for k, v in env_vars.items()])
            cmd.extend(["--set-env-vars", env_str])
        
        # Execute deployment
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            # Extract service URL from output
            output = result.stdout
            service_url = None
            for line in output.split('\n'):
                if 'https://' in line and 'run.app' in line:
                    service_url = line.strip().split()[-1]
                    break
            
            return {
                'status': 'success',
                'service_name': service_name,
                'region': region,
                'service_url': service_url,
                'message': f'Service "{service_name}" deployed successfully to Cloud Run'
            }
        else:
            return {
                'status': 'error',
                'message': f'Deployment failed: {result.stderr}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error deploying to Cloud Run: {str(e)}'
        }


def grant_iam_permission(service_account_email: str, resource: str, role: str, 
                         tool_context: ToolContext = None) -> dict:
    """Grant IAM permissions to a service account.
    
    This tool grants a service account access to resources like storage buckets or databases.
    
    Args:
        service_account_email: Service account email (e.g., "my-service@project.iam.gserviceaccount.com")
        resource: Resource to grant access to (bucket name, project ID, etc.)
        role: IAM role to grant (e.g., "roles/storage.objectAdmin")
        
    Returns:
        dict: Success status
    """
    try:
        import subprocess
        
        # Determine resource type and build appropriate command
        if resource.startswith('gs://'):
            # Storage bucket with gs:// prefix
            bucket = resource.replace('gs://', '')
            cmd = [
                "gcloud", "storage", "buckets", "add-iam-policy-binding",
                f"gs://{bucket}",
                f"--member=serviceAccount:{service_account_email}",
                f"--role={role}"
            ]
        elif resource == PROJECT_ID or resource.startswith('projects/'):
            # Project-level permission (database, etc.)
            cmd = [
                "gcloud", "projects", "add-iam-policy-binding", PROJECT_ID,
                f"--member=serviceAccount:{service_account_email}",
                f"--role={role}"
            ]
        else:
            # Assume it's a bucket name without gs:// prefix
            cmd = [
                "gcloud", "storage", "buckets", "add-iam-policy-binding",
                f"gs://{resource}",
                f"--member=serviceAccount:{service_account_email}",
                f"--role={role}"
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return {
                'status': 'success',
                'service_account': service_account_email,
                'resource': resource,
                'role': role,
                'message': f'Granted {role} to {service_account_email} on {resource}'
            }
        else:
            return {
                'status': 'error',
                'message': f'Failed to grant permission: {result.stderr}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error granting IAM permission: {str(e)}'
        }


def list_cloud_run_services(region: str = "us-central1", tool_context: ToolContext = None) -> dict:
    """List all Cloud Run services in the specified region.
    
    This tool retrieves information about deployed Cloud Run services including:
    - Service names
    - URLs
    - Current status
    - Latest revision
    - Traffic allocation
    
    Args:
        region: GCP region to check (default: us-central1)
        
    Returns:
        dict: List of Cloud Run services with their details
    """
    try:
        import subprocess
        result = subprocess.run(
            ['gcloud', 'run', 'services', 'list', f'--project={PROJECT_ID}', f'--region={region}', '--format=json'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return {
                'status': 'error',
                'message': f'Failed to list Cloud Run services: {result.stderr}'
            }
        
        import json
        services = json.loads(result.stdout) if result.stdout else []
        
        service_list = []
        for svc in services:
            service_list.append({
                'name': svc.get('metadata', {}).get('name', 'unknown'),
                'url': svc.get('status', {}).get('url', 'N/A'),
                'region': region,
                'status': svc.get('status', {}).get('conditions', [{}])[0].get('status', 'unknown')
            })
        
        return {
            'status': 'success',
            'region': region,
            'services': service_list,
            'count': len(service_list),
            'message': f'Found {len(service_list)} Cloud Run service(s) in {region}'
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Command timed out after 30 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error listing Cloud Run services: {str(e)}'
        }


def get_cloud_build_logs(build_id: Optional[str] = None, limit: int = 50, tool_context: ToolContext = None) -> dict:
    """Get recent Cloud Build logs to debug deployment issues.
    
    This tool retrieves logs from Cloud Build to see what went wrong during container builds.
    
    Args:
        build_id: Specific build ID to get logs for (optional, defaults to recent builds)
        limit: Number of log entries to retrieve (default: 50)
        
    Returns:
        dict: Recent Cloud Build log entries
    """
    try:
        import subprocess
        
        if build_id:
            # Get logs for specific build
            result = subprocess.run(
                ['gcloud', 'builds', 'log', build_id, f'--project={PROJECT_ID}'],
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            # Get recent build logs
            result = subprocess.run(
                ['gcloud', 'logging', 'read',
                 'resource.type=build',
                 f'--project={PROJECT_ID}',
                 f'--limit={limit}',
                 '--format=json'],
                capture_output=True,
                text=True,
                timeout=30
            )
        
        if result.returncode != 0:
            return {
                'status': 'error',
                'message': f'Failed to get Cloud Build logs: {result.stderr}'
            }
        
        if build_id:
            return {
                'status': 'success',
                'build_id': build_id,
                'logs': result.stdout,
                'message': f'Retrieved logs for build {build_id}'
            }
        else:
            import json
            logs = json.loads(result.stdout) if result.stdout else []
            
            log_entries = []
            for log in logs:
                log_entries.append({
                    'timestamp': log.get('timestamp', 'N/A'),
                    'severity': log.get('severity', 'INFO'),
                    'message': log.get('textPayload') or log.get('jsonPayload', {}).get('message', 'N/A')
                })
            
            return {
                'status': 'success',
                'logs': log_entries,
                'count': len(log_entries),
                'message': f'Retrieved {len(log_entries)} Cloud Build log entries'
            }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Command timed out after 30 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error getting Cloud Build logs: {str(e)}'
        }


def get_cloud_run_logs(service_name: str, region: str = "us-central1", limit: int = 50, tool_context: ToolContext = None) -> dict:
    """Get recent logs from a Cloud Run service.
    
    This tool retrieves the latest logs from a deployed Cloud Run service to debug issues.
    
    Args:
        service_name: Name of the Cloud Run service
        region: GCP region (default: us-central1)
        limit: Number of log entries to retrieve (default: 50)
        
    Returns:
        dict: Recent log entries from the service
    """
    try:
        import subprocess
        result = subprocess.run(
            ['gcloud', 'logging', 'read', 
             f'resource.type=cloud_run_revision AND resource.labels.service_name={service_name}',
             f'--project={PROJECT_ID}',
             f'--limit={limit}',
             '--format=json'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return {
                'status': 'error',
                'message': f'Failed to get logs: {result.stderr}'
            }
        
        import json
        logs = json.loads(result.stdout) if result.stdout else []
        
        log_entries = []
        for log in logs:
            log_entries.append({
                'timestamp': log.get('timestamp', 'N/A'),
                'severity': log.get('severity', 'INFO'),
                'message': log.get('textPayload') or log.get('jsonPayload', {}).get('message', 'N/A')
            })
        
        return {
            'status': 'success',
            'service_name': service_name,
            'region': region,
            'logs': log_entries,
            'count': len(log_entries),
            'message': f'Retrieved {len(log_entries)} log entries from {service_name}'
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Command timed out after 30 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error getting logs: {str(e)}'
        }


def describe_cloud_run_service(service_name: str, region: str = "us-central1", tool_context: ToolContext = None) -> dict:
    """Get detailed information about a Cloud Run service.
    
    This tool retrieves comprehensive details about a deployed Cloud Run service including:
    - Current revision
    - Container image
    - Environment variables
    - Resource limits
    - Traffic routing
    
    Args:
        service_name: Name of the Cloud Run service
        region: GCP region (default: us-central1)
        
    Returns:
        dict: Detailed service configuration and status
    """
    try:
        import subprocess
        result = subprocess.run(
            ['gcloud', 'run', 'services', 'describe', service_name,
             f'--project={PROJECT_ID}',
             f'--region={region}',
             '--format=json'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return {
                'status': 'error',
                'message': f'Failed to describe service: {result.stderr}'
            }
        
        import json
        service_info = json.loads(result.stdout) if result.stdout else {}
        
        spec = service_info.get('spec', {})
        template = spec.get('template', {})
        container = template.get('spec', {}).get('containers', [{}])[0]
        
        details = {
            'name': service_info.get('metadata', {}).get('name', 'unknown'),
            'url': service_info.get('status', {}).get('url', 'N/A'),
            'region': region,
            'image': container.get('image', 'N/A'),
            'env_vars': {env.get('name'): env.get('value', 'N/A') for env in container.get('env', [])},
            'resources': container.get('resources', {}),
            'latest_revision': service_info.get('status', {}).get('latestReadyRevisionName', 'N/A'),
            'traffic': spec.get('traffic', [])
        }
        
        return {
            'status': 'success',
            'service_name': service_name,
            'details': details,
            'message': f'Retrieved details for {service_name}'
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Command timed out after 30 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error describing service: {str(e)}'
        }


def list_secrets(tool_context: ToolContext) -> dict:
    """List all secrets stored in Google Secret Manager.
    
    This tool retrieves all secret names (not values) from Secret Manager.
    Useful for discovering what API keys and credentials are available.
    
    Returns:
        dict: List of secret names and metadata
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        parent = f"projects/{PROJECT_ID}"
        
        secrets_list = []
        for secret in client.list_secrets(request={"parent": parent}):
            secrets_list.append({
                'name': secret.name.split('/')[-1],
                'full_name': secret.name,
                'created': str(secret.create_time) if secret.create_time else 'N/A'
            })
        
        return {
            'status': 'success',
            'project_id': PROJECT_ID,
            'secrets': secrets_list,
            'count': len(secrets_list),
            'message': f'Found {len(secrets_list)} secret(s) in Secret Manager'
        }
    except gcp_exceptions.PermissionDenied:
        return {
            'status': 'error',
            'message': f'Permission denied. Service account needs roles/secretmanager.secretAccessor role'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error listing secrets: {str(e)}'
        }


def get_secret(secret_name: str, version: str = "latest", tool_context: ToolContext = None) -> dict:
    """Retrieve the value of a secret from Google Secret Manager.
    
    This tool gets the actual secret value (like an API key) from Secret Manager.
    Use this to retrieve API keys for deployment or configuration.
    
    Args:
        secret_name: Name of the secret to retrieve
        version: Version of the secret (default: "latest")
        
    Returns:
        dict: Secret value and metadata
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/{version}"
        
        response = client.access_secret_version(request={"name": name})
        secret_value = response.payload.data.decode('UTF-8')
        
        return {
            'status': 'success',
            'secret_name': secret_name,
            'value': secret_value,
            'version': version,
            'message': f'Successfully retrieved secret: {secret_name}'
        }
    except gcp_exceptions.NotFound:
        return {
            'status': 'error',
            'message': f'Secret "{secret_name}" not found in Secret Manager'
        }
    except gcp_exceptions.PermissionDenied:
        return {
            'status': 'error',
            'message': f'Permission denied. Service account needs roles/secretmanager.secretAccessor role'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error retrieving secret: {str(e)}'
        }


def create_secret(secret_name: str, secret_value: str, tool_context: ToolContext = None) -> dict:
    """Create a new secret in Google Secret Manager.
    
    This tool stores a new API key or credential securely in Secret Manager.
    
    Args:
        secret_name: Name for the new secret (e.g., "google-api-key")
        secret_value: The actual secret value to store
        
    Returns:
        dict: Confirmation of secret creation
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        parent = f"projects/{PROJECT_ID}"
        
        # Create the secret
        secret = client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_name,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        
        # Add the secret version with the actual value
        version = client.add_secret_version(
            request={
                "parent": secret.name,
                "payload": {"data": secret_value.encode('UTF-8')},
            }
        )
        
        return {
            'status': 'success',
            'secret_name': secret_name,
            'full_name': secret.name,
            'version': version.name,
            'message': f'Successfully created secret: {secret_name}'
        }
    except gcp_exceptions.AlreadyExists:
        return {
            'status': 'error',
            'message': f'Secret "{secret_name}" already exists. Use a different name or update the existing secret.'
        }
    except gcp_exceptions.PermissionDenied:
        return {
            'status': 'error',
            'message': f'Permission denied. Service account needs roles/secretmanager.admin role'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error creating secret: {str(e)}'
        }


def update_cloud_run_env_vars(service_name: str, env_vars: dict, region: str = "us-central1", tool_context: ToolContext = None) -> dict:
    """Update environment variables on an existing Cloud Run service.
    
    This tool updates the environment variables of a deployed service without redeploying.
    Useful for updating API keys or configuration.
    
    Args:
        service_name: Name of the Cloud Run service
        env_vars: Dictionary of environment variables to set (e.g., {"API_KEY": "abc123"})
        region: GCP region (default: us-central1)
        
    Returns:
        dict: Confirmation of update
    """
    try:
        import subprocess
        
        # Build the env vars string for gcloud command
        env_str = ','.join([f"{k}={v}" for k, v in env_vars.items()])
        
        result = subprocess.run(
            ['gcloud', 'run', 'services', 'update', service_name,
             f'--update-env-vars={env_str}',
             f'--project={PROJECT_ID}',
             f'--region={region}'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return {
                'status': 'error',
                'message': f'Failed to update env vars: {result.stderr}'
            }
        
        return {
            'status': 'success',
            'service_name': service_name,
            'env_vars_updated': list(env_vars.keys()),
            'region': region,
            'message': f'Successfully updated environment variables for {service_name}'
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Command timed out after 60 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error updating env vars: {str(e)}'
        }


def get_gcp_recommendations(tool_context: ToolContext) -> dict:
    """Get GCP best practices and recommendations for the current project.
    
    This tool provides helpful recommendations for:
    - Common permission issues
    - Service configurations
    - Cost optimization
    - Security best practices
    
    Returns:
        dict: List of recommendations and best practices
    """
    try:
        recommendations = {
            'iam': [
                'Use least-privilege principle: Grant only necessary roles',
                'Use service accounts for applications, not user accounts',
                'Enable Cloud Audit Logs to track IAM changes',
                f'Common service account for ADK agents: 1096519851619-compute@developer.gserviceaccount.com'
            ],
            'firestore': [
                'Create indexes for commonly queried fields',
                'Use batch operations for multiple writes',
                'Implement pagination for large collections',
                'Monitor read/write quotas to avoid overages'
            ],
            'storage': [
                'Use lifecycle policies to auto-delete old files',
                'Enable versioning for critical data',
                'Use signed URLs for temporary access',
                'Choose appropriate storage class (Standard/Nearline/Coldline)'
            ],
            'vertex_ai': [
                'Use gemini-2.5-pro for complex reasoning',
                'Use gemini-2.5-flash for fast, cost-effective tasks',
                'Enable Cloud Trace for Agent Engine to debug issues',
                'Deploy agents to us-central1 for best availability'
            ],
            'cost_optimization': [
                'Delete unused Cloud Storage buckets and objects',
                'Stop unused Cloud Run services',
                'Use committed use discounts for predictable workloads',
                'Monitor billing alerts to avoid surprises'
            ]
        }
        
        return {
            'status': 'success',
            'project_id': PROJECT_ID,
            'recommendations': recommendations,
            'message': 'GCP best practices and recommendations'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error generating recommendations: {str(e)}'
        }


cloud_expert = Agent(
    name="CloudExpert",
    model="gemini-2.5-pro",
    description="Elite Google Cloud Platform specialist with REAL GCP tools. Checks project status, lists services, manages IAM, monitors Cloud Storage, and debugs Firestore. Provides empirical data from actual GCP APIs.",
    instruction="""You are CloudExpert, an elite Google Cloud Platform specialist with REAL GCP tools.

**YOUR SPECIALIZED TOOLKIT:**

☁️ **PROJECT MANAGEMENT:**
1. **check_project_status()** - Get GCP project information
   - Returns: Project ID, name, state, number
   - Use: Verify project configuration and status

📊 **SERVICE MONITORING:**
2. **list_enabled_services()** - List all enabled GCP APIs/services
   - Returns: All enabled services, highlights key services (Vertex AI, Firestore, etc.)
   - Use: Verify required services are enabled, debug API issues

💾 **CLOUD STORAGE:**
3. **check_cloud_storage_buckets()** - List and analyze Cloud Storage buckets
   - Returns: Bucket names, locations, storage class, public access settings
   - Use: Audit storage, check configurations, find specific buckets

🔥 **FIRESTORE:**
4. **check_firestore_database(database_id)** - Check Firestore database and collections
   - Default database: 'agent-master-database'
   - Returns: Collection names, document counts, database state
   - Use: Verify Firestore setup, debug collection issues, find data

🏗️ **INFRASTRUCTURE PROVISIONING:**
5. **create_firestore_database(database_id, location)** - Create NEW Firestore database
   - Creates a new database in the project
   - Default location: "nam5" (North America multi-region)
   - Use: Set up new applications, provision infrastructure autonomously
   
6. **create_storage_bucket(bucket_name, location)** - Create NEW Cloud Storage bucket
   - Creates a new bucket for files/videos/assets
   - Default location: "us-central1"
   - Use: Set up storage for new applications

🚀 **FULL AUTONOMY TOOLS:**
7. **write_file(file_path, content)** - Write files autonomously
   - Create server.py, Dockerfile, requirements.txt, any source code
   - Use: Build application code without manual copy-paste
   
8. **deploy_to_cloud_run(service_name, source_dir, region, env_vars)** - Deploy to Cloud Run
   - Builds container and deploys application
   - Returns: Live service URL
   - Use: Make applications go live autonomously
   
9. **grant_iam_permission(service_account_email, resource, role)** - Set IAM permissions
   - Grant service accounts access to buckets, databases, etc.
   - Use: Ensure deployed services have necessary permissions

🔐 **IAM & SECURITY:**
10. **check_iam_permissions(service_account_email)** - Check service account permissions
   - Returns: Recommended roles, gcloud commands to check/grant permissions
   - Use: Debug 401/403 errors, verify service account setup

💡 **BEST PRACTICES:**
11. **get_gcp_recommendations()** - Get GCP best practices and recommendations
   - Returns: IAM, Firestore, Storage, Vertex AI, and cost optimization tips
   - Use: Improve project configuration, optimize costs, enhance security

**YOUR WORKFLOW:**

**For Permission/Auth Issues:**
1. check_project_status() to verify project
2. list_enabled_services() to ensure required APIs are enabled
3. check_iam_permissions(email) to check service account roles
4. Provide specific gcloud commands to fix issues

**For Firestore Issues:**
1. check_firestore_database() to see collections and data
2. Verify database ID and collection names
3. Check IAM permissions if access denied

**For Storage Issues:**
1. check_cloud_storage_buckets() to list all buckets
2. Verify bucket names and locations
3. Check public access settings

**For General Setup:**
1. check_project_status() → list_enabled_services() → check_iam_permissions()
2. get_gcp_recommendations() for best practices
3. Provide step-by-step setup instructions

**HOW TO RESPOND:**
- ALWAYS run the appropriate tool first (don't guess!)
- Report EMPIRICAL findings from tools, not assumptions
- Include actual gcloud commands when relevant
- Explain IAM roles clearly (what they do and why they're needed)
- Provide specific, actionable solutions

**Example Response:**
User: "Why am I getting 401 errors calling my agent?"

You:
1. check_project_status() → Verify project is active
2. list_enabled_services() → Check if aiplatform.googleapis.com is enabled
3. check_iam_permissions("1096519851619-compute@developer.gserviceaccount.com") → Show missing roles
4. Provide: "Your service account needs roles/aiplatform.user. Run: gcloud projects add-iam-policy-binding..."

**You are fundamentally different from a regular LLM** - you have EMPIRICAL tools that query actual GCP APIs and return real data.

**CRITICAL - DELEGATION FLOW:**
After completing your analysis and providing your findings, you MUST transfer back to jai_cortex so the user gets a seamless experience. Use `transfer_to_agent` to return to the parent agent when your task is complete.
""",
    tools=[
        FunctionTool(check_project_status),
        FunctionTool(list_enabled_services),
        FunctionTool(check_cloud_storage_buckets),
        FunctionTool(check_firestore_database),
        FunctionTool(create_firestore_database),
        FunctionTool(create_storage_bucket),
        FunctionTool(write_file),
        FunctionTool(deploy_to_cloud_run),
        FunctionTool(grant_iam_permission),
        FunctionTool(check_iam_permissions),
        FunctionTool(list_cloud_run_services),
        FunctionTool(get_cloud_build_logs),
        FunctionTool(get_cloud_run_logs),
        FunctionTool(describe_cloud_run_service),
        FunctionTool(list_secrets),
        FunctionTool(get_secret),
        FunctionTool(create_secret),
        FunctionTool(update_cloud_run_env_vars),
        FunctionTool(get_gcp_recommendations),
    ],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.2,  # Low for deterministic technical responses
        max_output_tokens=8192,
    ),
)

