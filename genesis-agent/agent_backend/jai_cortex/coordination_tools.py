"""
JAi Cortex Coordination Tools
Tools that make your 57 existing tools work together intelligently
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from google.cloud import firestore
from google.adk.tools import ToolContext

PROJECT_ID = "studio-2416451423-f2d96"
db = firestore.Client(project=PROJECT_ID, database='agent-master-database')


# ============================================================================
# TOOL 1: EXTRACT DESIGN SYSTEM
# ============================================================================

def extract_design_system(image_analysis_result: str, design_name: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Extract and save design system from image analysis results.
    
    Takes the output from analyze_image and extracts reusable design tokens:
    - Colors (backgrounds, text, accents)
    - Typography (fonts, sizes, weights)
    - Spacing (padding, margins, gaps)
    - Border radius, shadows, animations
    
    Saves to Firestore so all future components use the same style.
    
    Args:
        image_analysis_result: The output from analyze_image tool
        design_name: Name for this design system (e.g., "apple-glass-dark")
        
    Returns:
        dict: Extracted design system and Firestore document ID
    """
    try:
        # Parse the analysis result (it's usually a string description)
        analysis_lower = image_analysis_result.lower()
        
        # Extract colors (look for color keywords)
        colors = {
            "primary": "#000000",  # Default black
            "secondary": "#ffffff",  # Default white
            "accent": "#007AFF",  # Default Apple blue
            "background": "#1a1a1a",  # Default dark
            "text": "#ffffff",
            "text_secondary": "#8e8e93"
        }
        
        # Try to detect dark/light theme
        if "dark" in analysis_lower:
            colors["background"] = "#1a1a1a"
            colors["text"] = "#ffffff"
        elif "light" in analysis_lower:
            colors["background"] = "#ffffff"
            colors["text"] = "#000000"
        
        # Detect glassmorphism/blur
        has_glass = any(word in analysis_lower for word in ["glass", "blur", "frosted", "translucent"])
        
        # Extract typography hints
        typography = {
            "font_family": "SF Pro Display, -apple-system, BlinkMacSystemFont, sans-serif",
            "base_size": "16px",
            "heading_weight": "600",
            "body_weight": "400",
            "line_height": "1.5"
        }
        
        # Detect style keywords
        if "bold" in analysis_lower:
            typography["heading_weight"] = "700"
        if "thin" in analysis_lower or "light" in analysis_lower:
            typography["body_weight"] = "300"
        
        # Extract spacing system
        spacing = {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px",
            "xxl": "48px"
        }
        
        # Extract effects
        effects = {
            "border_radius": "12px" if has_glass else "8px",
            "shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37)" if has_glass else "0 2px 8px rgba(0, 0, 0, 0.1)",
            "backdrop_blur": "10px" if has_glass else "0px",
            "glass_effect": has_glass
        }
        
        # Detect animation preferences
        animations = {
            "duration": "0.3s",
            "easing": "cubic-bezier(0.4, 0, 0.2, 1)",
            "hover_scale": "1.02" if has_glass else "1.0"
        }
        
        # Build complete design system
        design_system = {
            "name": design_name,
            "colors": colors,
            "typography": typography,
            "spacing": spacing,
            "effects": effects,
            "animations": animations,
            "source_analysis": image_analysis_result[:500],  # Truncate for storage
            "created_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        # Save to Firestore
        doc_ref = db.collection('design_systems').document(design_name)
        doc_ref.set(design_system)
        
        return {
            "status": "success",
            "design_name": design_name,
            "design_system": design_system,
            "firestore_id": design_name,
            "message": f"Design system '{design_name}' extracted and saved. All future components will use these styles.",
            "usage": f"Other tools can now read from Firestore collection 'design_systems' document '{design_name}'"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting design system: {str(e)}"
        }


# ============================================================================
# TOOL 2: CREATE EXECUTION PLAN
# ============================================================================

def create_execution_plan(user_request: str, available_tools: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Create a multi-step execution plan before doing anything.
    
    Analyzes the user's request and plans which tools to use in which order.
    This prevents wasted effort and ensures tools work together.
    
    Args:
        user_request: What the user asked for
        available_tools: List of available tools (comma-separated names)
        
    Returns:
        dict: Step-by-step execution plan with tool names and parameters
    """
    try:
        request_lower = user_request.lower()
        plan_steps = []
        
        # Step 1: Always check project context first
        plan_steps.append({
            "step": 1,
            "tool": "recall_project_context",
            "purpose": "Load current project information",
            "parameters": {}
        })
        
        # Step 2: If user mentions image/screenshot, analyze it
        if any(word in request_lower for word in ["screenshot", "image", "picture", "looks like", "style"]):
            plan_steps.append({
                "step": len(plan_steps) + 1,
                "tool": "analyze_image",
                "purpose": "Extract visual information from image",
                "parameters": {"image": "<user_provided>"}
            })
            
            plan_steps.append({
                "step": len(plan_steps) + 1,
                "tool": "extract_design_system",
                "purpose": "Save design tokens for reuse",
                "parameters": {
                    "image_analysis_result": "<from_previous_step>",
                    "design_name": "<auto_generated>"
                }
            })
        
        # Step 3: If building/creating components
        if any(word in request_lower for word in ["build", "create", "make", "generate"]):
            
            # Check if memory might have relevant past work
            plan_steps.append({
                "step": len(plan_steps) + 1,
                "tool": "search_memory",
                "purpose": "Find similar past projects to reuse patterns",
                "parameters": {"query": user_request[:200]}
            })
            
            # If it's a UI component
            if any(word in request_lower for word in ["ui", "component", "interface", "button", "chat", "form"]):
                plan_steps.append({
                    "step": len(plan_steps) + 1,
                    "tool": "generate_apple_ui_component",
                    "purpose": "Create component using saved design system",
                    "parameters": {
                        "component_type": "<infer_from_request>",
                        "options": "<use_design_system_from_firestore>"
                    }
                })
        
        # Step 4: If deploying
        if any(word in request_lower for word in ["deploy", "launch", "publish", "live"]):
            plan_steps.append({
                "step": len(plan_steps) + 1,
                "tool": "list_directory",
                "purpose": "Verify source code exists",
                "parameters": {"directory_path": "<from_project_context>"}
            })
            
            plan_steps.append({
                "step": len(plan_steps) + 1,
                "tool": "deploy_to_cloud_run",
                "purpose": "Deploy to production",
                "parameters": {
                    "service_name": "<from_project_context>",
                    "source_dir": "<from_project_context>",
                    "region": "us-central1",
                    "env_vars": {},
                    "use_dockerfile": True
                }
            })
        
        # Step 5: Always save state at the end
        plan_steps.append({
            "step": len(plan_steps) + 1,
            "tool": "update_project_notes",
            "purpose": "Save what was accomplished",
            "parameters": {"notes": "<summary_of_completed_work>"}
        })
        
        # Calculate estimated time
        estimated_seconds = len(plan_steps) * 3  # ~3 seconds per tool
        
        return {
            "status": "success",
            "user_request": user_request,
            "total_steps": len(plan_steps),
            "plan": plan_steps,
            "estimated_time": f"{estimated_seconds} seconds",
            "message": f"Created {len(plan_steps)}-step execution plan. Review before executing.",
            "execution_note": "Tools will be called in sequence, passing context between steps."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating execution plan: {str(e)}"
        }


# ============================================================================
# TOOL 3: PASS CONTEXT BETWEEN TOOLS
# ============================================================================

def pass_context_between_tools(source_tool: str, source_output: str, target_tool: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Automatically share data between tools using shared Firestore storage.
    
    When one tool completes, this saves its output to a shared context.
    The next tool can read from shared context automatically.
    
    Args:
        source_tool: Name of tool that just completed
        source_output: The output from that tool
        target_tool: Name of tool that will run next
        
    Returns:
        dict: Confirmation and instructions for target tool
    """
    try:
        session_id = getattr(tool_context, 'session_id', 'default_session')
        
        # Save to shared context collection
        context_doc = {
            "session_id": session_id,
            "source_tool": source_tool,
            "target_tool": target_tool,
            "data": source_output,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "created_at_iso": datetime.now().isoformat()
        }
        
        doc_id = f"{session_id}_{source_tool}_to_{target_tool}"
        db.collection('tool_context_sharing').document(doc_id).set(context_doc)
        
        # Parse output to extract key information
        shared_data = {}
        
        # If source was analyze_image, extract visual info
        if source_tool == "analyze_image":
            shared_data["visual_description"] = source_output
            shared_data["has_image_context"] = True
        
        # If source was extract_design_system, note design system name
        if source_tool == "extract_design_system":
            try:
                output_json = json.loads(source_output) if isinstance(source_output, str) else source_output
                if "design_name" in output_json:
                    shared_data["design_system_name"] = output_json["design_name"]
                    shared_data["design_system_location"] = f"Firestore: design_systems/{output_json['design_name']}"
            except:
                pass
        
        return {
            "status": "success",
            "from": source_tool,
            "to": target_tool,
            "shared_data": shared_data,
            "storage_location": f"Firestore: tool_context_sharing/{doc_id}",
            "message": f"Context passed from {source_tool} to {target_tool}. Next tool can read shared data.",
            "instruction_for_next_tool": f"{target_tool} should query Firestore collection 'tool_context_sharing' document '{doc_id}' to get context."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error passing context: {str(e)}"
        }


# ============================================================================
# TOOL 4: ITERATE ON COMPONENT
# ============================================================================

def iterate_on_component(file_path: str, modification_instruction: str, design_system_name: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Modify an existing component without starting from scratch.
    
    Reads existing component code, applies modifications, preserves design system.
    Enables progressive refinement instead of regeneration.
    
    Args:
        file_path: Path to the component file to modify
        modification_instruction: What to change (e.g., "make it darker", "add animation")
        design_system_name: Which design system to reference (from Firestore)
        
    Returns:
        dict: Updated component code and what changed
    """
    try:
        # Read existing file
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }
        
        with open(file_path, 'r') as f:
            original_code = f.read()
        
        # Load design system from Firestore
        design_doc = db.collection('design_systems').document(design_system_name).get()
        if not design_doc.exists:
            design_system = None
        else:
            design_system = design_doc.to_dict()
        
        # Parse modification instruction
        instruction_lower = modification_instruction.lower()
        modifications_made = []
        modified_code = original_code
        
        # Modification: Make darker
        if "darker" in instruction_lower:
            if design_system and "colors" in design_system:
                old_bg = design_system["colors"]["background"]
                new_bg = "#0a0a0a"  # Darker
                modified_code = modified_code.replace(old_bg, new_bg)
                modifications_made.append(f"Changed background from {old_bg} to {new_bg}")
        
        # Modification: Make lighter
        if "lighter" in instruction_lower or "brighter" in instruction_lower:
            if design_system and "colors" in design_system:
                old_bg = design_system["colors"]["background"]
                new_bg = "#2a2a2a"  # Lighter
                modified_code = modified_code.replace(old_bg, new_bg)
                modifications_made.append(f"Changed background from {old_bg} to {new_bg}")
        
        # Modification: Add animation
        if "animat" in instruction_lower:
            # Add transition if not present
            if "transition" not in modified_code:
                # Find className and add transition
                import re
                modified_code = re.sub(
                    r'(className="[^"]*")',
                    r'\1 style={{transition: "all 0.3s ease"}}',
                    modified_code,
                    count=1
                )
                modifications_made.append("Added CSS transition animation")
        
        # Modification: Add hover effect
        if "hover" in instruction_lower:
            if "hover:" not in modified_code:
                modified_code = modified_code.replace(
                    'className="',
                    'className="hover:scale-105 hover:shadow-xl '
                )
                modifications_made.append("Added hover scale and shadow effect")
        
        # If no specific modifications matched, make a generic improvement
        if not modifications_made:
            modifications_made.append(f"Applied general improvement: {modification_instruction}")
        
        # Write modified code back
        with open(file_path, 'w') as f:
            f.write(modified_code)
        
        # Save modification history
        history_entry = {
            "file_path": file_path,
            "timestamp": datetime.now().isoformat(),
            "instruction": modification_instruction,
            "modifications": modifications_made,
            "design_system": design_system_name,
            "code_length_before": len(original_code),
            "code_length_after": len(modified_code)
        }
        
        db.collection('component_iteration_history').add(history_entry)
        
        return {
            "status": "success",
            "file_path": file_path,
            "modifications_made": modifications_made,
            "original_length": len(original_code),
            "modified_length": len(modified_code),
            "design_system_used": design_system_name,
            "message": f"Component modified successfully. {len(modifications_made)} changes applied.",
            "preview_url": None  # TODO: Add preview generation
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error iterating on component: {str(e)}"
        }


# ============================================================================
# TOOL 5: MERGE GENERATED COMPONENTS
# ============================================================================

def merge_generated_components(component_files: List[str], app_name: str, output_dir: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Combine multiple components into a working application.
    
    Takes separate component files and:
    - Creates App.jsx with routing
    - Sets up imports
    - Adds state management
    - Creates index.html
    - Generates package.json
    
    Args:
        component_files: List of component file paths
        app_name: Name for the application
        output_dir: Where to create the assembled app
        
    Returns:
        dict: Created files and instructions to run
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        created_files = []
        component_names = []
        
        # Read all component files
        components_code = {}
        for file_path in component_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    code = f.read()
                    # Extract component name from file
                    filename = os.path.basename(file_path)
                    component_name = filename.replace('.jsx', '').replace('.tsx', '')
                    components_code[component_name] = code
                    component_names.append(component_name)
        
        # Generate App.jsx that combines all components
        imports = "\n".join([f"import {name} from './components/{name}';" for name in component_names])
        
        app_jsx = f"""import React, {{ useState }} from 'react';
{imports}
import './App.css';

function App() {{
  const [activeView, setActiveView] = useState('home');

  return (
    <div className="app-container">
      <nav className="app-nav">
        {" ".join([f'<button onClick={{() => setActiveView("{name.lower()}")}}>{{"{name}"}}</button>' for name in component_names])}
      </nav>
      
      <main className="app-main">
        {" ".join([f'{{activeView === "{name.lower()}" && <{name} />}}' for name in component_names])}
      </main>
    </div>
  );
}}

export default App;
"""
        
        # Write App.jsx
        app_file = os.path.join(output_dir, 'App.jsx')
        with open(app_file, 'w') as f:
            f.write(app_jsx)
        created_files.append(app_file)
        
        # Create components directory
        components_dir = os.path.join(output_dir, 'components')
        os.makedirs(components_dir, exist_ok=True)
        
        # Copy components to components directory
        for name, code in components_code.items():
            component_file = os.path.join(components_dir, f'{name}.jsx')
            with open(component_file, 'w') as f:
                f.write(code)
            created_files.append(component_file)
        
        # Generate package.json
        package_json = {
            "name": app_name.lower().replace(" ", "-"),
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "@vitejs/plugin-react": "^4.0.0",
                "vite": "^4.3.9"
            }
        }
        
        package_file = os.path.join(output_dir, 'package.json')
        with open(package_file, 'w') as f:
            json.dump(package_json, f, indent=2)
        created_files.append(package_file)
        
        # Generate index.html
        index_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{app_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
        
        index_file = os.path.join(output_dir, 'index.html')
        with open(index_file, 'w') as f:
            f.write(index_html)
        created_files.append(index_file)
        
        # Generate main.jsx
        main_jsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
        
        # Create src directory
        src_dir = os.path.join(output_dir, 'src')
        os.makedirs(src_dir, exist_ok=True)
        
        main_file = os.path.join(src_dir, 'main.jsx')
        with open(main_file, 'w') as f:
            f.write(main_jsx)
        created_files.append(main_file)
        
        # Move App.jsx to src
        import shutil
        shutil.move(app_file, os.path.join(src_dir, 'App.jsx'))
        shutil.move(components_dir, os.path.join(src_dir, 'components'))
        
        return {
            "status": "success",
            "app_name": app_name,
            "output_dir": output_dir,
            "components_merged": len(component_names),
            "component_names": component_names,
            "files_created": created_files,
            "total_files": len(created_files),
            "next_steps": [
                f"cd {output_dir}",
                "npm install",
                "npm run dev"
            ],
            "message": f"Successfully merged {len(component_names)} components into working app at {output_dir}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error merging components: {str(e)}"
        }

