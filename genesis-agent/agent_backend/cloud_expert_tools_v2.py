
from google.cloud.devtools import cloudbuild_v1

def get_latest_failed_build_logs(project_id: str) -> dict:
    """Fetches the logs for the most recent failed build in a GCP project.

    Args:
        project_id: The Google Cloud project ID.

    Returns:
        A dictionary containing the logs of the latest failed build or an error message.
    """
    try:
        client = cloudbuild_v1.CloudBuildClient()
        parent = f'projects/{project_id}'

        # List builds, most recent first
        builds = client.list_builds(project_id=project_id)

        latest_failed_build = None
        for build in builds:
            if build.status == cloudbuild_v1.Build.Status.FAILURE:
                latest_failed_build = build
                break

        if not latest_failed_build:
            return {"status": "success", "message": "No failed builds found."}

        # Fetch the logs for the latest failed build
        # Note: In a real implementation, this would stream the log content.
        # For this tool, we'll return the log URL available in the build object.
        log_url = latest_failed_build.log_url
        build_id = latest_failed_build.id
        
        # A more advanced version would use the storage client to download the log file directly.
        # For now, providing the direct URL is the most useful action.

        return {
            "status": "success",
            "build_id": build_id,
            "log_url": log_url,
            "message": f"Found latest failed build ({build_id}). Logs are available at the URL."
        }

    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve build logs: {str(e)}"}

