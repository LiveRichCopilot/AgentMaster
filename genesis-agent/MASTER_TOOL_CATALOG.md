# JAi CORTEX MASTER TOOL CATALOG
**Total Tools: 116**  
**Last Updated: 2025-10-05**

This is the complete catalog of every tool available to JAi Cortex and its specialist agents. Use this as your reference guide.

---

## 📊 QUICK STATS

| Category | Tool Count |
|----------|-----------|
| Memory & Context | 6 |
| Cloud Infrastructure | 14 |
| Deployment & Build | 6 |
| Debugging & Diagnostics | 7 |
| File Operations | 6 |
| Media Processing | 5 |
| Web & Search | 5 |
| Secret Management | 3 |
| Database | 4 |
| Meta-Agent | 5 |
| Code Analysis | 8 |
| Communication | 3 |
| Agent Coordination | 8 |
| Other | 36 |

---

## 🧠 MEMORY & CONTEXT (6 tools)

### `recall_project_context()`
**What it does:** Finds what project you're currently working on (searches ALL past sessions)  
**When to use:** At the start of EVERY conversation to remember context  
**Returns:** Project name, path, description, last updated

### `remember_project_context(project_name, project_path, description)`
**What it does:** Saves the current project so agents never forget it  
**When to use:** When starting a new project or switching projects  
**Returns:** Confirmation that project was saved

### `update_project_notes(notes)`
**What it does:** Add notes to current project (progress, issues, decisions)  
**When to use:** After completing major tasks or making decisions  
**Returns:** Updated project context

### `search_memory(query)`
**What it does:** Semantic search across ALL past conversations using vector embeddings  
**When to use:** User asks "do you remember when..." or need past context  
**Returns:** Top 5 relevant past conversations with timestamps

### `pass_context_between_tools(source_tool, source_output, target_tool)`
**What it does:** Automatically shares data between tools using Firestore  
**When to use:** Multi-step workflows where tool B needs tool A's output  
**Returns:** Confirmation that context was saved

### `get_conversation_context(user_id, limit)`
**What it does:** Retrieves recent conversation history for a user  
**When to use:** Need to understand conversation flow or user's recent requests  
**Returns:** List of recent messages with timestamps

---

## ☁️ CLOUD INFRASTRUCTURE (14 tools)

### `check_project_status()`
**What it does:** Gets GCP project info (ID, name, state, number)  
**When to use:** Verify project configuration, get project number for IAM  
**Returns:** Project ID, display name, project number, state

### `list_enabled_services()`
**What it does:** Lists all enabled GCP APIs/services  
**When to use:** Verify required services are enabled, debug API errors  
**Returns:** List of enabled services with names and states

### `check_cloud_storage_buckets()`
**What it does:** Lists all Cloud Storage buckets with details  
**When to use:** Audit storage, find specific buckets, check configurations  
**Returns:** Bucket names, locations, storage class, public access settings

### `create_storage_bucket(bucket_name, location)`
**What it does:** Creates a new Cloud Storage bucket  
**When to use:** Setting up storage for new applications  
**Returns:** Bucket name and location

### `check_firestore_database(database_id)`
**What it does:** Checks Firestore database and lists collections  
**When to use:** Verify Firestore setup, debug collection issues  
**Returns:** Collection names, document counts, database state

### `create_firestore_database(database_id, location)`
**What it does:** Creates a NEW Firestore database  
**When to use:** Setting up new applications that need a database  
**Returns:** Database ID and creation status

### `query_firestore_collection(collection_name, limit, database_id)`
**What it does:** Queries a Firestore collection and returns documents  
**When to use:** Retrieve data from Firestore, inspect collection contents  
**Returns:** List of documents with their data

### `analyze_collection_schema(collection_name, sample_size, database_id)`
**What it does:** Analyzes the structure and schema of a Firestore collection  
**When to use:** Understand data structure, find inconsistencies  
**Returns:** Schema analysis with field types and patterns

### `get_collection_stats(collection_name, database_id)`
**What it does:** Gets detailed statistics for a Firestore collection  
**When to use:** Understand collection size, document counts, data distribution  
**Returns:** Document count, size, field statistics

### `grant_iam_permission(service_account_email, resource, role)`
**What it does:** Grants IAM permissions to a service account  
**When to use:** Fix permission errors, enable service account access  
**Returns:** Confirmation of permission grant

### `check_iam_permissions(service_account_email)`
**What it does:** Checks what IAM roles a service account has  
**When to use:** Debug permission issues, verify access before deploying  
**Returns:** List of roles and deployment readiness status

### `optimize_firestore_query(query_description)`
**What it does:** Analyzes a Firestore query and suggests optimizations  
**When to use:** Slow queries, need to improve performance  
**Returns:** Optimization suggestions and best practices

### `check_firestore_indexes(database_id)`
**What it does:** Gets Firestore index recommendations  
**When to use:** Query performance issues, need composite indexes  
**Returns:** Index recommendations and best practices

### `get_gcp_recommendations()`
**What it does:** Gets GCP best practices and recommendations  
**When to use:** Setting up new projects, optimizing existing infrastructure  
**Returns:** Security, cost, and performance recommendations

---

## 🚀 DEPLOYMENT & BUILD (6 tools)

### `deploy_to_cloud_run(service_name, source_dir, region, env_vars, use_dockerfile)`
**What it does:** Deploys an application to Cloud Run  
**When to use:** Make applications go live, deploy backends/APIs  
**Returns:** Live service URL

### `list_cloud_run_services(region)`
**What it does:** Lists all Cloud Run services in a region  
**When to use:** See what's deployed, find service names  
**Returns:** List of services with URLs and statuses

### `describe_cloud_run_service(service_name, region)`
**What it does:** Gets detailed info about a Cloud Run service  
**When to use:** Debug deployment issues, check service configuration  
**Returns:** Service details, env vars, resource limits, status

### `get_cloud_run_logs(service_name, region, limit)`
**What it does:** Gets recent logs from a Cloud Run service  
**When to use:** Debug runtime errors, see what's happening in production  
**Returns:** Recent log entries with timestamps

### `get_cloud_build_logs(build_id, limit)`
**What it does:** Gets Cloud Build logs for a deployment  
**When to use:** Debug build failures, see why deployment failed  
**Returns:** Build log entries

### `update_cloud_run_env_vars(service_name, env_vars, region)`
**What it does:** Updates environment variables on a Cloud Run service  
**When to use:** Add API keys, change configuration without redeploying  
**Returns:** Confirmation of update

---

## 🔍 DEBUGGING & DIAGNOSTICS (7 tools)

### `debug_deployment_failure(service_name, error_message)`
**What it does:** AUTO-DIAGNOSES Cloud Run failures by reading actual logs  
**When to use:** IMMEDIATELY after ANY deployment fails  
**Returns:** Root cause, actual error, specific fix recommendations

### `verify_before_deploy(source_dir)`
**What it does:** Pre-flight checks BEFORE deploying (syntax, files, port config)  
**When to use:** BEFORE every deployment to catch issues early  
**Returns:** Deploy readiness status, issues found, confidence score

### `test_container_locally(source_dir, port)`
**What it does:** Tests Docker container locally (10s test vs 5min Cloud Run)  
**When to use:** Before deploying, when deployment keeps failing  
**Returns:** Build success, run success, responds to requests status

### `parse_cloud_run_error(service_name)`
**What it does:** Parses Cloud Run logs to find ACTUAL errors (not generic messages)  
**When to use:** When error message is generic, need root cause  
**Returns:** Parsed errors, warnings, root causes identified

### `validate_deployment_success(service_url, expected_status)`
**What it does:** ACTUALLY tests if deployed service works (don't trust deploy tool)  
**When to use:** AFTER every deployment to verify it's actually working  
**Returns:** Actually working status, response preview, issues found

### `analyze_failure_pattern(service_name, attempts)`
**What it does:** Detects when stuck in a failure loop (same error 3+ times)  
**When to use:** After 3+ failed attempts with same error  
**Returns:** Failure pattern detected, alternative approaches

### `save_debug_note(title, content)`
**What it does:** Saves debugging notes and solutions  
**When to use:** After solving a tricky issue, want to remember solution  
**Returns:** Note saved confirmation

---

## 📁 FILE OPERATIONS (6 tools)

### `write_file(file_path, content)`
**What it does:** Writes content to a file (persistent on real file system)  
**When to use:** Create source code, Dockerfiles, configs, any files  
**Returns:** File written confirmation

### `read_file_content(file_path)`
**What it does:** Reads a file and returns its contents  
**When to use:** Verify file exists, inspect file content, debug issues  
**Returns:** File contents as string

### `list_directory(directory_path)`
**What it does:** Lists all files and subdirectories in a directory  
**When to use:** See what files exist, verify directory structure  
**Returns:** List of files and directories

### `find_directory(search_name, start_path)`
**What it does:** Searches for directories by name in file system  
**When to use:** Don't know exact path, need to locate a directory  
**Returns:** Matching directory paths

### `write_file_simple(file_path, content)`
**What it does:** Simplified file writing (same as write_file)  
**When to use:** Create files quickly without extra options  
**Returns:** File written confirmation

---

## 🎬 MEDIA PROCESSING (5 tools)

### `analyze_image()`
**What it does:** Analyzes image content using Google Cloud Vision AI  
**When to use:** User uploads image, need object detection, scene understanding  
**Returns:** Labels, objects detected, logos, safe search results

### `extract_text_from_image()`
**What it does:** OCR text extraction from images  
**When to use:** Extract text from screenshots, documents, photos  
**Returns:** Extracted text, word count

### `analyze_video()`
**What it does:** Analyzes video content using Video Intelligence API  
**When to use:** User uploads video, need scene detection, labels  
**Returns:** Video labels, scenes, confidence scores

### `transcribe_video()`
**What it does:** Transcribes speech from video files  
**When to use:** Extract spoken words from videos, meeting recordings  
**Returns:** Full transcript, word count, GCS URI

### `extract_audio_from_video()`
**What it does:** Extracts audio track from video files  
**When to use:** Prepare video for transcription, get audio separately  
**Returns:** Audio file path, format, sample rate

---

## 🌐 WEB & SEARCH (5 tools)

### `simple_search(query)`
**What it does:** Basic web search (placeholder, to be enhanced)  
**When to use:** Quick info lookup, basic searches  
**Returns:** Search results

### `advanced_web_research(query, num_sources)`
**What it does:** Comprehensive research with multi-source synthesis (Perplexity mode)  
**When to use:** User needs in-depth research, multiple sources, citations  
**Returns:** Synthesized answer with citations and source list

### `get_search_snippets(query, num_results)`
**What it does:** Web search with result snippets  
**When to use:** Need search results with context snippets  
**Returns:** Search results with titles, URLs, snippets

### `search_tool_libraries(query, sources)`
**What it does:** Searches GitHub, PyPI for existing tool solutions  
**When to use:** Before building new tool, find existing solutions  
**Returns:** Found tools, repos, adaptation recommendations

### `create_vector_search_index()`
**What it does:** Creates Vertex AI Vector Search index for memory  
**When to use:** Setting up semantic search for conversation memory  
**Returns:** Index creation status

---

## 🔐 SECRET MANAGEMENT (3 tools)

### `list_secrets()`
**What it does:** Lists all secrets in Google Secret Manager  
**When to use:** Find API keys, see what secrets exist  
**Returns:** List of secret names

### `get_secret(secret_name, version)`
**What it does:** Retrieves the VALUE of a secret from Secret Manager  
**When to use:** Need API key for deployment, retrieve credentials  
**Returns:** Secret value (sensitive!)

### `create_secret(secret_name, secret_value)`
**What it does:** Creates a new secret in Secret Manager  
**When to use:** Store API keys, credentials securely  
**Returns:** Secret creation confirmation

---

## 🗄️ DATABASE (4 tools)

### `call_database_expert(task)`
**What it does:** Delegates to DatabaseExpert specialist agent  
**When to use:** Complex database queries, schema design, optimization  
**Returns:** DatabaseExpert's response

### `get_database_recommendations()`
**What it does:** Gets Firestore best practices  
**When to use:** Setting up new database, optimizing existing one  
**Returns:** Best practices and recommendations

---

## 🤖 META-AGENT (5 tools)

### `analyze_task_for_agent_needs(task_description)`
**What it does:** Figures out what kind of agent is needed for a task  
**When to use:** User needs specialized agent, complex task  
**Returns:** Agent blueprint with recommended tools

### `generate_agent_from_blueprint(blueprint, output_dir)`
**What it does:** Creates a complete agent from blueprint  
**When to use:** After analyzing task needs, ready to build agent  
**Returns:** Agent files created, directory path

### `clone_agent_with_modifications(source_agent, new_agent, keep_tools, remove_tools, add_tools)`
**What it does:** Clones existing agent and customizes it  
**When to use:** Need variant of existing agent with different capabilities  
**Returns:** New agent blueprint

### `spawn_temporary_agent(task, required_tools, lifetime_minutes)`
**What it does:** Creates single-use agent for specific task  
**When to use:** One-time task, don't need permanent agent  
**Returns:** Temporary agent ID and task info

### `generate_tool_from_description(tool_name, description, inputs, outputs)`
**What it does:** GENERATES NEW TOOLS on demand  
**When to use:** Need tool that doesn't exist, identified capability gap  
**Returns:** Generated tool code, file path, next steps

---

## 💻 CODE ANALYSIS (8 tools)

### `analyze_github_repo(repo_url, branch)`
**What it does:** Clones and analyzes GitHub repository  
**When to use:** User asks about GitHub repo, need to understand codebase  
**Returns:** Repo structure, file list, analysis

### `read_github_file(repo_url, file_path, branch)`
**What it does:** Reads specific file from GitHub repo  
**When to use:** Need to inspect specific file without cloning whole repo  
**Returns:** File contents

### `analyze_code_file(filename, code_content, issue_description)`
**What it does:** Analyzes code for bugs, errors, improvements  
**When to use:** User uploads code with issue, need debugging  
**Returns:** Analysis with issues found and recommendations

### `lint_python_code(code)`
**What it does:** Runs flake8 and pylint on Python code  
**When to use:** Check code style, find bugs before running  
**Returns:** Linting issues and suggestions

### `format_python_code(code)`
**What it does:** Auto-formats Python code to PEP 8 standards  
**When to use:** Clean up code formatting  
**Returns:** Formatted code

### `scan_python_security(code)`
**What it does:** Runs Bandit security scanner on Python code  
**When to use:** Check for security vulnerabilities  
**Returns:** Security issues found

### `analyze_code_complexity(code)`
**What it does:** Analyzes code complexity and maintainability  
**When to use:** Understand code quality, find complex areas  
**Returns:** Complexity metrics and recommendations

---

## 💬 COMMUNICATION (3 tools)

### `review_communication(recent_turns)`
**What it does:** Analyzes conversation quality (like Zoom's communication scoring)  
**When to use:** User asks "how is our communication?" or wants quality score  
**Returns:** Communication score (0-100), quality rating, recommendations

### `get_cognitive_profile(user_id, days)`
**What it does:** Gets user's communication patterns and preferences  
**When to use:** Understand how user prefers to communicate  
**Returns:** Cognitive profile with patterns and preferences

### `analyze_conversation(user_id, session_id, recent_turns)`
**What it does:** Analyzes recent conversation turns for quality  
**When to use:** Generate communication score, identify issues  
**Returns:** Score, metrics, recommendations

---

## 🔗 AGENT COORDINATION (8 tools)

### `agent_to_agent_message(to_agent, message, include_context)`
**What it does:** Sends message from one agent to another  
**When to use:** Direct agent-to-agent communication  
**Returns:** Message delivery confirmation

### `broadcast_to_all_agents(message, metadata)`
**What it does:** Broadcasts message to all registered agents  
**When to use:** System-wide announcements, new tool available  
**Returns:** Broadcast confirmation, recipient count

### `register_agent_capability(agent_name, capabilities, endpoint, cost_per_call)`
**What it does:** Registers agent's capabilities in global registry  
**When to use:** New agent created, announce what it can do  
**Returns:** Registration confirmation

### `discover_available_agents(task)`
**What it does:** Finds agents that can help with a task  
**When to use:** Need specialist agent, don't know which one  
**Returns:** Matching agents with capabilities

### `agent_handoff_queue(task, agent_sequence)`
**What it does:** Creates multi-agent workflow queue  
**When to use:** Complex task requiring multiple agents in sequence  
**Returns:** Workflow ID and queue created

### `list_all_agents()`
**What it does:** Lists all agents in ecosystem  
**When to use:** See what agents exist, their capabilities  
**Returns:** List of agents with capabilities and status

### `agent_dependency_graph()`
**What it does:** Shows how agents interact and depend on each other  
**When to use:** Understand agent relationships, debug delegation issues  
**Returns:** Dependency graph structure

### `agent_self_audit(days)`
**What it does:** Agent reviews its own performance  
**When to use:** Periodic self-assessment, identify improvement areas  
**Returns:** Performance report with recommendations

---

## 🎨 UI & DESIGN (5 tools)

### `extract_design_system(image_analysis_result, design_name)`
**What it does:** Extracts colors, fonts, spacing from image analysis  
**When to use:** User uploads design screenshot, want to replicate style  
**Returns:** Design system saved to Firestore

### `generate_apple_ui_component(component_type, options)`
**What it does:** Generates Apple iOS 18 Liquid Glass UI components (React/JSX)  
**When to use:** Building UI with Apple glassmorphic design  
**Returns:** Component code

### `generate_css_styles(style_type, options)`
**What it does:** Generates modern CSS (gradients, animations, glassmorphism)  
**When to use:** Need specific CSS effects  
**Returns:** CSS code

### `setup_tailwind_css(project_dir)`
**What it does:** Installs and configures Tailwind CSS in React/Vite project  
**When to use:** Setting up new project with Tailwind  
**Returns:** Setup status

### `iterate_on_component(file_path, modification_instruction, design_system_name)`
**What it does:** Modifies existing component without starting from scratch  
**When to use:** User says "make it darker/lighter/animated"  
**Returns:** Modified component code

---

## 🛠️ DEVELOPMENT TOOLS (5 tools)

### `execute_shell_command(command, working_dir, timeout)`
**What it does:** Executes shell commands (npm, git, mkdir, etc.)  
**When to use:** Run terminal commands, build projects  
**Returns:** Command output, exit code

### `create_execution_plan(user_request, available_tools)`
**What it does:** Creates multi-step execution plan BEFORE doing anything  
**When to use:** Complex tasks, want to show user the plan first  
**Returns:** Step-by-step plan with tools and estimated time

### `merge_generated_components(component_files, app_name, output_dir)`
**What it does:** Combines multiple components into working application  
**When to use:** After generating multiple components, need complete app  
**Returns:** Complete app with routing and state

### `check_system_status()`
**What it does:** Runs diagnostics on all backend services  
**When to use:** Verify system health, debug service issues  
**Returns:** Status of all services (Firestore, Storage, Vision, Speech)

### `save_note(title, content)`
**What it does:** Saves notes permanently (retrieve via DatabaseExpert)  
**When to use:** User asks to remember something  
**Returns:** Note saved confirmation

---

## 🔄 SELF-MODIFICATION (4 tools)

### `analyze_conversation_patterns(user_id, days)`
**What it does:** Learns user preferences from conversation history  
**When to use:** Understand how user communicates, adapt behavior  
**Returns:** Patterns identified, preferences learned

### `update_agent_personality(observations)`
**What it does:** Updates agent behavior based on observations  
**When to use:** After learning user preferences, want to adapt  
**Returns:** Personality updates applied

### `version_control_agent(action, version)`
**What it does:** Saves/restores agent state versions  
**When to use:** Save working state, rollback to previous version  
**Returns:** Version saved or restored

### `combine_tools_into_macro(macro_name, tool_sequence, description)`
**What it does:** Combines multiple tools into single shortcut  
**When to use:** User repeatedly does same sequence of tools  
**Returns:** Macro tool created

---

## 📚 TOOL TEMPLATES (3 tools)

### `save_tool_template(category, template_name, pattern)`
**What it does:** Saves reusable tool pattern  
**When to use:** Created useful tool pattern, want to reuse  
**Returns:** Template saved

### `import_tool_from_template(template_name, new_tool_name, customizations)`
**What it does:** Creates new tool from saved template  
**When to use:** Need similar tool to one already built  
**Returns:** New tool generated from template

### `reverse_engineer_tool_from_example(code_example, tool_name)`
**What it does:** Learns tool pattern from example code  
**When to use:** User shows code example, want to make it a tool  
**Returns:** Tool generated from example

---

## 🔧 UTILITY TOOLS (5 tools)

### `optimize_existing_tool(tool_name, optimization_goal)`
**What it does:** Improves existing tool's performance or reliability  
**When to use:** Tool is slow or failing, need to fix it  
**Returns:** Optimized tool code

### `benchmark_tool_performance(tool_names, test_iterations)`
**What it does:** Tests tool speed and reliability  
**When to use:** Want to know which tools are slow or failing  
**Returns:** Performance metrics for each tool

### `infer_tools_from_conversation(conversation_history)`
**What it does:** Identifies needed tools from conversation patterns  
**When to use:** User keeps asking for same thing, might need new tool  
**Returns:** Tool needs identified

### `analyze_missing_capabilities(attempted_action)`
**What it does:** Figures out what tool is needed when agent can't do something  
**When to use:** Agent tries to do something but doesn't have the tool  
**Returns:** Missing capability identified, tool proposal

### `find_notes()`
**What it does:** Finds all saved notes  
**When to use:** User asks "show me my notes"  
**Returns:** List of saved notes

---

## 📞 SPECIALIST AGENT CALLERS (4 tools)

### `call_code_master(task)`
**What it does:** Delegates to CodeMaster for coding help  
**When to use:** Code writing, debugging, GitHub analysis, security review  
**Returns:** CodeMaster's response

### `call_cloud_expert(task)`
**What it does:** Delegates to CloudExpert for GCP help  
**When to use:** Cloud infrastructure, deployment, IAM, Cloud Storage  
**Returns:** CloudExpert's response

### `call_automation_wizard(task)`
**What it does:** Delegates to AutomationWizard for workflow automation  
**When to use:** Repetitive tasks, CI/CD, process optimization  
**Returns:** AutomationWizard's response

### `call_vision_analyzer(task)`
**What it does:** Delegates to VisionAnalyzer for advanced visual analysis  
**When to use:** Complex image understanding, UI/UX analysis  
**Returns:** VisionAnalyzer's response

---

## 🎯 WHEN TO USE WHAT

### **Starting a Conversation**
1. `recall_project_context()` - ALWAYS first
2. `search_memory(query)` - If user references past work

### **Deploying Something**
1. `verify_before_deploy(source_dir)` - BEFORE deploying
2. `deploy_to_cloud_run(...)` - Deploy
3. If fails → `debug_deployment_failure(...)` - Diagnose
4. `validate_deployment_success(url)` - AFTER deploying

### **User Asks About Past Work**
1. `search_memory(query)` - Search conversations
2. `find_notes()` - Find saved notes
3. `call_database_expert("show my notes")` - Get structured data

### **Building Something New**
1. `create_execution_plan(request, tools)` - Plan first
2. `analyze_image()` - If user sends screenshot
3. `extract_design_system(...)` - Save design
4. `generate_apple_ui_component(...)` - Build components
5. `merge_generated_components(...)` - Combine into app

### **Something's Broken**
1. `get_cloud_run_logs(service)` - See what's happening
2. `parse_cloud_run_error(service)` - Find root cause
3. `check_iam_permissions(account)` - Verify permissions
4. `describe_cloud_run_service(service)` - Check config

### **Need a Tool That Doesn't Exist**
1. `analyze_missing_capabilities(action)` - Identify gap
2. `search_tool_libraries(query)` - Look for existing solution
3. `generate_tool_from_description(...)` - Create new tool

---

## 💡 PRO TIPS

**Memory is Your Superpower:**
- Call `recall_project_context()` at the start of EVERY conversation
- Use `search_memory()` when user says "remember when..."
- Call `update_project_notes()` after major milestones

**Debug Before Guessing:**
- ALWAYS call `debug_deployment_failure()` when deployment fails
- NEVER guess at fixes - read the logs first
- Use `verify_before_deploy()` to catch issues early

**Coordinate Complex Tasks:**
- Use `create_execution_plan()` for multi-step tasks
- Use `pass_context_between_tools()` to share data
- Use `merge_generated_components()` to combine outputs

**Learn and Improve:**
- Use `agent_self_audit()` periodically
- Use `analyze_conversation_patterns()` to learn user preferences
- Use `optimize_existing_tool()` when tools fail repeatedly

---

**This catalog is your reference guide. Bookmark it. Search it. Use it when you forget what tools you have.**
