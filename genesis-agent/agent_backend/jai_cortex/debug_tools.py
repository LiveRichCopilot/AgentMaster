"""
JAi Cortex Debug & Verification Tools
Tools that ACTUALLY diagnose problems instead of guessing
"""

import os
import re
import json
import subprocess
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.cloud import firestore, logging as cloud_logging
from google.adk.tools import ToolContext

PROJECT_ID = "studio-2416451423-f2d96"
db = firestore.Client(project=PROJECT_ID, database='agent-master-database')


# ============================================================================
# 1. AUTO-DEBUG DEPLOYMENT FAILURES
# ============================================================================

def debug_deployment_failure(service_name: str, error_message: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Automatically diagnose Cloud Run deployment failures by reading actual logs.
    
    When deployment fails, DON'T GUESS. This tool:
    1. Extracts the log URL from error message
    2. Fetches actual Cloud Run startup logs
    3. Parses for real errors (ImportError, port issues, crashes)
    4. Identifies root cause
    5. Proposes SPECIFIC fix based on ACTUAL error
    
    Args:
        service_name: Name of the failed Cloud Run service
        error_message: The generic error message from deployment
        
    Returns:
        dict: Root cause analysis and specific fix recommendations
    """
    try:
        diagnosis = {
            "service_name": service_name,
            "generic_error": error_message,
            "root_cause": None,
            "actual_error": None,
            "recommended_fixes": [],
            "log_url": None
        }
        
        # Extract log URL from error message if present
        log_url_match = re.search(r'https://console\.cloud\.google\.com/logs/[^\s]+', error_message)
        if log_url_match:
            diagnosis["log_url"] = log_url_match.group(0)
        
        # Fetch actual Cloud Run logs
        print(f"🔍 Fetching logs for {service_name}...")
        
        try:
            result = subprocess.run(
                [
                    'gcloud', 'logging', 'read',
                    f'resource.type="cloud_run_revision" AND resource.labels.service_name="{service_name}"',
                    '--limit', '50',
                    '--format', 'json',
                    '--project', PROJECT_ID
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                logs = json.loads(result.stdout)
                
                # Parse logs for actual errors
                errors_found = []
                for log_entry in logs:
                    text_payload = log_entry.get('textPayload', '')
                    json_payload = log_entry.get('jsonPayload', {})
                    
                    # Look for Python errors
                    if 'Traceback' in text_payload or 'Error' in text_payload:
                        errors_found.append(text_payload)
                    
                    # Look for common issues
                    if 'ImportError' in text_payload or 'ModuleNotFoundError' in text_payload:
                        diagnosis["root_cause"] = "Missing Python dependency"
                        diagnosis["actual_error"] = text_payload
                        diagnosis["recommended_fixes"].append(
                            "Add missing package to requirements.txt and redeploy"
                        )
                    
                    elif 'Permission denied' in text_payload or 'PERMISSION_DENIED' in text_payload:
                        diagnosis["root_cause"] = "IAM permissions missing"
                        diagnosis["actual_error"] = text_payload
                        diagnosis["recommended_fixes"].append(
                            "Grant required IAM role to Cloud Run service account"
                        )
                    
                    elif 'Connection refused' in text_payload or 'Failed to connect' in text_payload:
                        diagnosis["root_cause"] = "Database/service connection failure"
                        diagnosis["actual_error"] = text_payload
                        diagnosis["recommended_fixes"].append(
                            "Verify Firestore/database is accessible from Cloud Run",
                            "Check if GCP_PROJECT env var is set"
                        )
                    
                    elif 'PORT' in text_payload or 'port' in text_payload.lower():
                        diagnosis["root_cause"] = "Port binding issue"
                        diagnosis["actual_error"] = text_payload
                        diagnosis["recommended_fixes"].append(
                            "Ensure app listens on PORT environment variable (default 8080)"
                        )
                    
                    elif 'Syntax' in text_payload or 'SyntaxError' in text_payload:
                        diagnosis["root_cause"] = "Python syntax error"
                        diagnosis["actual_error"] = text_payload
                        diagnosis["recommended_fixes"].append(
                            "Fix syntax error in source code before deploying"
                        )
                
                # If we found errors but didn't categorize them
                if errors_found and not diagnosis["root_cause"]:
                    diagnosis["root_cause"] = "Application crash on startup"
                    diagnosis["actual_error"] = "\n".join(errors_found[:3])
                    diagnosis["recommended_fixes"].append(
                        "Review full error logs and fix application code"
                    )
            
            else:
                diagnosis["root_cause"] = "Could not fetch logs"
                diagnosis["recommended_fixes"].append(
                    "Check Cloud Run console manually for logs"
                )
        
        except Exception as log_error:
            diagnosis["root_cause"] = f"Log fetch failed: {str(log_error)}"
        
        # If still no root cause, provide generic guidance
        if not diagnosis["root_cause"]:
            if "timeout" in error_message.lower():
                diagnosis["root_cause"] = "Container failed to start within timeout"
                diagnosis["recommended_fixes"] = [
                    "Check if app is actually listening on PORT env var",
                    "Verify Dockerfile CMD/ENTRYPOINT is correct",
                    "Test container locally first"
                ]
            else:
                diagnosis["root_cause"] = "Unknown - logs unavailable"
                diagnosis["recommended_fixes"] = [
                    "Use test_container_locally to debug",
                    "Check Cloud Run console for detailed logs"
                ]
        
        return {
            "status": "success",
            "diagnosis": diagnosis,
            "message": f"Root cause: {diagnosis['root_cause']}",
            "next_action": diagnosis["recommended_fixes"][0] if diagnosis["recommended_fixes"] else "Manual investigation required"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Debug failed: {str(e)}"
        }


# ============================================================================
# 2. PRE-DEPLOYMENT VERIFICATION
# ============================================================================

def verify_before_deploy(source_dir: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Pre-flight checks before deploying to Cloud Run.
    
    Catches issues BEFORE wasting time on failed deployments.
    
    Args:
        source_dir: Path to source code directory
        
    Returns:
        dict: Deploy readiness status and issues found
    """
    try:
        issues = []
        warnings = []
        checks_passed = 0
        checks_total = 0
        
        # Check 1: Directory exists
        checks_total += 1
        if not os.path.exists(source_dir):
            issues.append(f"Source directory does not exist: {source_dir}")
        else:
            checks_passed += 1
        
        # Check 2: Has Dockerfile or requirements.txt
        checks_total += 1
        has_dockerfile = os.path.exists(os.path.join(source_dir, 'Dockerfile'))
        has_requirements = os.path.exists(os.path.join(source_dir, 'requirements.txt'))
        
        if not has_dockerfile and not has_requirements:
            issues.append("No Dockerfile or requirements.txt found")
        else:
            checks_passed += 1
        
        # Check 3: If has requirements.txt, check syntax
        if has_requirements:
            checks_total += 1
            req_file = os.path.join(source_dir, 'requirements.txt')
            try:
                with open(req_file, 'r') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Basic validation
                            if '==' not in line and '>=' not in line and line.count('/') > 2:
                                warnings.append(f"Line {i} in requirements.txt looks suspicious: {line}")
                checks_passed += 1
            except Exception as e:
                issues.append(f"Could not read requirements.txt: {str(e)}")
        
        # Check 4: If has Dockerfile, check PORT usage
        if has_dockerfile:
            checks_total += 1
            dockerfile_path = os.path.join(source_dir, 'Dockerfile')
            try:
                with open(dockerfile_path, 'r') as f:
                    dockerfile_content = f.read()
                    
                    # Check if EXPOSE or PORT is mentioned
                    if 'EXPOSE' not in dockerfile_content and 'PORT' not in dockerfile_content:
                        warnings.append("Dockerfile doesn't mention PORT - Cloud Run requires listening on $PORT")
                    
                    # Check for hardcoded ports
                    if '8080' in dockerfile_content or '8000' in dockerfile_content:
                        warnings.append("Dockerfile has hardcoded port - should use $PORT env var")
                    
                checks_passed += 1
            except Exception as e:
                issues.append(f"Could not read Dockerfile: {str(e)}")
        
        # Check 5: Find main server file
        checks_total += 1
        server_files = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file in ['server.py', 'main.py', 'app.py', 'api.py']:
                    server_files.append(os.path.join(root, file))
        
        if not server_files:
            warnings.append("No obvious server file found (server.py, main.py, app.py)")
        else:
            checks_passed += 1
            
            # Check 6: Verify server file syntax
            checks_total += 1
            for server_file in server_files[:1]:  # Check first one
                try:
                    result = subprocess.run(
                        ['python3', '-m', 'py_compile', server_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        checks_passed += 1
                    else:
                        issues.append(f"Syntax error in {os.path.basename(server_file)}: {result.stderr}")
                except Exception as e:
                    warnings.append(f"Could not verify syntax: {str(e)}")
        
        # Determine deploy readiness
        deploy_ready = len(issues) == 0
        confidence = (checks_passed / checks_total * 100) if checks_total > 0 else 0
        
        return {
            "status": "success",
            "deploy_ready": deploy_ready,
            "confidence": round(confidence, 1),
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "issues": issues,
            "warnings": warnings,
            "recommendation": "Safe to deploy" if deploy_ready else "Fix issues before deploying",
            "message": f"Pre-flight checks: {checks_passed}/{checks_total} passed"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Verification failed: {str(e)}"
        }


# ============================================================================
# 3. TEST CONTAINER LOCALLY
# ============================================================================

def test_container_locally(source_dir: str, port: int, tool_context: ToolContext) -> Dict[str, Any]:
    """Test Docker container locally before deploying to Cloud Run.
    
    10 second local test vs 5 minute Cloud Run deployment cycle.
    
    Args:
        source_dir: Path to directory with Dockerfile
        port: Port to test on (default 8080)
        
    Returns:
        dict: Container test results
    """
    try:
        import time
        import uuid
        
        # Generate unique image name
        image_name = f"test-container-{uuid.uuid4().hex[:8]}"
        
        results = {
            "build_success": False,
            "run_success": False,
            "responds_to_requests": False,
            "build_output": "",
            "run_output": "",
            "test_url": f"http://localhost:{port}",
            "errors": []
        }
        
        # Step 1: Build image
        print(f"🔨 Building Docker image: {image_name}")
        build_result = subprocess.run(
            ['docker', 'build', '-t', image_name, source_dir],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        results["build_output"] = build_result.stdout + build_result.stderr
        
        if build_result.returncode != 0:
            results["errors"].append(f"Docker build failed: {build_result.stderr}")
            return {
                "status": "success",
                "results": results,
                "message": "Container build failed",
                "recommendation": "Fix Dockerfile errors before deploying"
            }
        
        results["build_success"] = True
        
        # Step 2: Run container
        print(f"🚀 Running container on port {port}")
        run_result = subprocess.Popen(
            [
                'docker', 'run', '--rm',
                '-p', f'{port}:{port}',
                '-e', f'PORT={port}',
                image_name
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for container to start
        time.sleep(5)
        
        # Check if container is still running
        if run_result.poll() is not None:
            # Container exited
            stdout, stderr = run_result.communicate()
            results["run_output"] = stdout + stderr
            results["errors"].append(f"Container exited immediately: {stderr}")
            
            # Cleanup
            subprocess.run(['docker', 'rmi', image_name], capture_output=True)
            
            return {
                "status": "success",
                "results": results,
                "message": "Container crashed on startup",
                "recommendation": "Fix application errors before deploying"
            }
        
        results["run_success"] = True
        
        # Step 3: Test if it responds
        print(f"🧪 Testing http://localhost:{port}")
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            results["responds_to_requests"] = True
            results["status_code"] = response.status_code
            results["response_preview"] = response.text[:200]
        except Exception as req_error:
            results["errors"].append(f"Container not responding: {str(req_error)}")
        
        # Cleanup: Stop container
        run_result.terminate()
        run_result.wait(timeout=5)
        
        # Remove image
        subprocess.run(['docker', 'rmi', image_name], capture_output=True)
        
        # Final verdict
        if results["responds_to_requests"]:
            message = "✅ Container works locally - safe to deploy"
            recommendation = "Deploy to Cloud Run"
        elif results["run_success"]:
            message = "⚠️ Container runs but doesn't respond to requests"
            recommendation = "Check if app is listening on correct port"
        else:
            message = "❌ Container fails locally"
            recommendation = "Fix errors before deploying"
        
        return {
            "status": "success",
            "results": results,
            "message": message,
            "recommendation": recommendation
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Local test failed: {str(e)}"
        }


# ============================================================================
# 4. SMART LOG PARSER
# ============================================================================

def parse_cloud_run_error(service_name: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Parse Cloud Run logs to find actual errors (not generic messages).
    
    Args:
        service_name: Cloud Run service name
        
    Returns:
        dict: Parsed errors and root cause
    """
    try:
        # Fetch logs
        result = subprocess.run(
            [
                'gcloud', 'logging', 'read',
                f'resource.type="cloud_run_revision" AND resource.labels.service_name="{service_name}"',
                '--limit', '100',
                '--format', 'json',
                '--project', PROJECT_ID
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return {
                "status": "error",
                "message": f"Could not fetch logs: {result.stderr}"
            }
        
        logs = json.loads(result.stdout)
        
        # Parse for errors
        errors = []
        warnings = []
        info = []
        
        for log_entry in logs:
            severity = log_entry.get('severity', 'INFO')
            text = log_entry.get('textPayload', '')
            timestamp = log_entry.get('timestamp', '')
            
            if severity == 'ERROR' or 'Error' in text or 'error' in text:
                errors.append({
                    "timestamp": timestamp,
                    "message": text[:500]
                })
            elif severity == 'WARNING' or 'Warning' in text:
                warnings.append({
                    "timestamp": timestamp,
                    "message": text[:500]
                })
            else:
                info.append({
                    "timestamp": timestamp,
                    "message": text[:500]
                })
        
        # Identify patterns
        root_causes = []
        
        for error in errors:
            msg = error["message"]
            
            if 'ImportError' in msg or 'ModuleNotFoundError' in msg:
                root_causes.append("Missing Python dependency")
            elif 'Permission' in msg or 'PERMISSION_DENIED' in msg:
                root_causes.append("IAM permissions issue")
            elif 'Connection' in msg or 'connect' in msg.lower():
                root_causes.append("Database/service connection failure")
            elif 'PORT' in msg or 'port' in msg:
                root_causes.append("Port binding issue")
            elif 'Syntax' in msg:
                root_causes.append("Code syntax error")
        
        return {
            "status": "success",
            "service_name": service_name,
            "errors_found": len(errors),
            "warnings_found": len(warnings),
            "errors": errors[:10],
            "warnings": warnings[:5],
            "root_causes": list(set(root_causes)),
            "message": f"Found {len(errors)} errors in logs",
            "recommendation": root_causes[0] if root_causes else "Review error logs manually"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Log parsing failed: {str(e)}"
        }


# ============================================================================
# 5. DEPLOYMENT SUCCESS VALIDATOR
# ============================================================================

def validate_deployment_success(service_url: str, expected_status: int, tool_context: ToolContext) -> Dict[str, Any]:
    """Actually test if deployed service works (don't trust deploy tool).
    
    Args:
        service_url: URL of deployed Cloud Run service
        expected_status: Expected HTTP status code (default 200)
        
    Returns:
        dict: Actual deployment status
    """
    try:
        validation = {
            "service_url": service_url,
            "actually_working": False,
            "status_code": None,
            "response_preview": None,
            "response_time_ms": None,
            "issues": []
        }
        
        # Test the URL
        import time
        start_time = time.time()
        
        try:
            response = requests.get(service_url, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            validation["status_code"] = response.status_code
            validation["response_time_ms"] = round(response_time, 2)
            validation["response_preview"] = response.text[:500]
            
            # Check if it's actually working
            if response.status_code == expected_status:
                validation["actually_working"] = True
            elif response.status_code == 503:
                validation["issues"].append("Service unavailable (503) - container not starting")
            elif response.status_code == 404:
                validation["issues"].append("Not found (404) - wrong URL or service not deployed")
            elif response.status_code >= 500:
                validation["issues"].append(f"Server error ({response.status_code}) - application crashing")
            else:
                validation["issues"].append(f"Unexpected status code: {response.status_code}")
            
            # Check response content
            if "Hello" in response.text and "World" in response.text:
                validation["issues"].append("⚠️ Deployed placeholder 'Hello World' app instead of actual app")
            
        except requests.exceptions.Timeout:
            validation["issues"].append("Request timeout - service not responding")
        except requests.exceptions.ConnectionError:
            validation["issues"].append("Connection failed - service not reachable")
        except Exception as req_error:
            validation["issues"].append(f"Request failed: {str(req_error)}")
        
        # Verdict
        if validation["actually_working"]:
            message = "✅ Deployment successful and working"
            recommendation = "Service is live and responding correctly"
        else:
            message = "❌ Deployment failed or not working"
            recommendation = validation["issues"][0] if validation["issues"] else "Debug required"
        
        return {
            "status": "success",
            "validation": validation,
            "message": message,
            "recommendation": recommendation
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Validation failed: {str(e)}"
        }


# ============================================================================
# 6. ANALYZE FAILURE PATTERNS
# ============================================================================

def analyze_failure_pattern(service_name: str, attempts: int, tool_context: ToolContext) -> Dict[str, Any]:
    """Detect when agent is stuck in a failure loop.
    
    If same error happens 3+ times, suggest different approach.
    
    Args:
        service_name: Service being deployed
        attempts: Number of failed attempts
        
    Returns:
        dict: Pattern analysis and alternative approaches
    """
    try:
        # Check Firestore for recent deployment attempts
        recent_attempts = db.collection('deployment_attempts')\
            .where('service_name', '==', service_name)\
            .order_by('timestamp', direction=firestore.Query.DESCENDING)\
            .limit(10)\
            .stream()
        
        attempts_list = [doc.to_dict() for doc in recent_attempts]
        
        # Analyze patterns
        error_types = {}
        for attempt in attempts_list:
            error = attempt.get('error_type', 'unknown')
            error_types[error] = error_types.get(error, 0) + 1
        
        # Detect loops
        stuck_in_loop = False
        repeated_error = None
        
        for error_type, count in error_types.items():
            if count >= 3:
                stuck_in_loop = True
                repeated_error = error_type
                break
        
        alternatives = []
        
        if stuck_in_loop:
            if repeated_error == "port_binding":
                alternatives = [
                    "Use gcloud run deploy with explicit --port flag",
                    "Test container locally first with test_container_locally",
                    "Verify Dockerfile EXPOSE matches PORT env var"
                ]
            elif repeated_error == "iam_permissions":
                alternatives = [
                    "Grant roles/run.admin to deploying user",
                    "Use service account with proper permissions",
                    "Check if service account has roles/datastore.user"
                ]
            elif repeated_error == "container_crash":
                alternatives = [
                    "Read actual logs with parse_cloud_run_error",
                    "Test locally with test_container_locally",
                    "Deploy minimal Hello World first to test infrastructure"
                ]
            else:
                alternatives = [
                    "Try manual gcloud run deploy command",
                    "Test container locally first",
                    "Deploy to different region"
                ]
        
        return {
            "status": "success",
            "service_name": service_name,
            "total_attempts": len(attempts_list),
            "stuck_in_loop": stuck_in_loop,
            "repeated_error": repeated_error,
            "error_counts": error_types,
            "alternative_approaches": alternatives,
            "message": f"Detected failure loop: {repeated_error}" if stuck_in_loop else "No pattern detected",
            "recommendation": alternatives[0] if alternatives else "Continue current approach"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Pattern analysis failed: {str(e)}"
        }
