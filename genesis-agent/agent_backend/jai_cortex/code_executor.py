"""
Code Executor Tool for JAi
Allows JAi to run Python code and see the actual results.
"""

import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any
from google.adk.tools import ToolContext


def execute_python_code(code: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute Python code and return the output.
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        dict: Execution results with stdout, stderr, and exit code
    """
    try:
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute the code
        result = subprocess.run(
            ['python3', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Clean up
        os.unlink(temp_file)
        
        success = result.returncode == 0
        
        return {
            'status': 'success' if success else 'error',
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'output': result.stdout if success else result.stderr
        }
        
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return {
            'status': 'error',
            'error': f'Code execution timed out after {timeout} seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': f'Failed to execute code: {str(e)}'
        }


def execute_shell_command(command: str, working_dir: str, timeout: int, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Execute a shell command (npm, git, mkdir, etc.) and return the output.
    
    Use this for:
    - npm/yarn commands (npm install, npm create vite, etc.)
    - git commands (git init, git clone, etc.)
    - File operations (mkdir, cp, mv, etc.)
    - Build commands (npm run build, etc.)
    
    Args:
        command: Shell command to execute (e.g., "npm create vite@latest my-app")
        working_dir: Directory to run the command in (optional, defaults to current dir)
        timeout: Maximum execution time in seconds (default: 300 = 5 minutes)
        tool_context: ADK tool context (optional)
        
    Returns:
        dict: Command execution results with stdout, stderr, and exit code
    """
    try:
        # Set working directory (use current dir if empty string)
        cwd = working_dir if working_dir else os.getcwd()
        
        # Execute the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        
        success = result.returncode == 0
        
        return {
            'status': 'success' if success else 'error',
            'exit_code': result.returncode,
            'command': command,
            'working_dir': cwd,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'output': result.stdout if success else result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'error': f'Command timed out after {timeout} seconds',
            'command': command
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': f'Failed to execute command: {str(e)}',
            'command': command
        }


def setup_tailwind_css(project_dir: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Install and configure Tailwind CSS in a React/Vite project.
    
    This tool:
    1. Installs Tailwind CSS and dependencies
    2. Initializes Tailwind config
    3. Updates CSS files with Tailwind directives
    
    Args:
        project_dir: Path to the project directory
        tool_context: ADK tool context (optional)
        
    Returns:
        dict: Installation status and configuration details
    """
    try:
        steps = []
        
        # Step 1: Install Tailwind CSS
        install_cmd = "npm install -D tailwindcss postcss autoprefixer"
        install_result = subprocess.run(
            install_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=project_dir
        )
        steps.append({
            'step': 'install_dependencies',
            'success': install_result.returncode == 0,
            'output': install_result.stdout if install_result.returncode == 0 else install_result.stderr
        })
        
        if install_result.returncode != 0:
            return {
                'status': 'error',
                'error': 'Failed to install Tailwind dependencies',
                'details': install_result.stderr,
                'steps': steps
            }
        
        # Step 2: Initialize Tailwind config
        init_cmd = "npx tailwindcss init -p"
        init_result = subprocess.run(
            init_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=project_dir
        )
        steps.append({
            'step': 'init_config',
            'success': init_result.returncode == 0,
            'output': init_result.stdout if init_result.returncode == 0 else init_result.stderr
        })
        
        # Step 3: Update tailwind.config.js with content paths
        config_path = Path(project_dir) / 'tailwind.config.js'
        if config_path.exists():
            tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(tailwind_config)
            steps.append({'step': 'update_config', 'success': True})
        
        # Step 4: Update main CSS file with Tailwind directives
        css_files = [
            Path(project_dir) / 'src' / 'index.css',
            Path(project_dir) / 'src' / 'App.css'
        ]
        
        tailwind_directives = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
        
        for css_file in css_files:
            if css_file.exists():
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write(tailwind_directives)
                steps.append({'step': f'update_{css_file.name}', 'success': True})
                break
        
        return {
            'status': 'success',
            'message': 'Tailwind CSS installed and configured successfully',
            'project_dir': project_dir,
            'steps': steps,
            'next_steps': [
                'Start using Tailwind classes in your components',
                'Run "npm run dev" to start development server'
            ]
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f'Failed to setup Tailwind CSS: {str(e)}',
            'steps': steps if 'steps' in locals() else []
        }


def generate_css_styles(style_type: str, options: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Generate modern CSS styles including gradients, animations, glassmorphism, and more.
    
    Style Types:
    - "glassmorphism" - Apple-style glass effect with blur
    - "gradient" - Modern gradient backgrounds
    - "animation" - CSS animations (fade, slide, bounce, etc.)
    - "button" - Modern button styles
    - "card" - Card component styles
    - "navbar" - Navigation bar styles
    
    Args:
        style_type: Type of CSS to generate
        options: Additional options (e.g., "pink-turquoise" for gradient colors)
        tool_context: ADK tool context (optional)
        
    Returns:
        dict: Generated CSS code and usage instructions
    """
    try:
        css_templates = {
            "glassmorphism": """/* Apple Glassmorphic Effect */
.glass-container {
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.glass-light {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}""",
            
            "gradient": """/* Modern Gradient Backgrounds */
.gradient-pink-turquoise {
  background: linear-gradient(135deg, #FF006E 0%, #00F5FF 100%);
}

.gradient-animated {
  background: linear-gradient(270deg, #FF006E, #8B5CF6, #00F5FF, #10B981);
  background-size: 800% 800%;
  animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 20s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}""",
            
            "animation": """/* Modern CSS Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInRight {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.8; }
}

.animate-fade-in { animation: fadeIn 0.6s ease-out; }
.animate-slide-in { animation: slideInRight 0.5s ease-out; }
.animate-pulse { animation: pulse 2s ease-in-out infinite; }""",
            
            "button": """/* Modern Button Styles */
.btn-glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 12px 24px;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-glass:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.btn-gradient {
  background: linear-gradient(135deg, #FF006E 0%, #8B5CF6 100%);
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 0, 110, 0.4);
}""",
            
            "card": """/* Modern Card Styles */
.card-glass {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s ease;
}

.card-glass:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  border-color: rgba(255, 255, 255, 0.2);
}""",
            
            "navbar": """/* Apple-style Navigation Bar */
.navbar-glass {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 16px 32px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-glass nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}"""
        }
        
        if style_type not in css_templates:
            return {
                'status': 'error',
                'error': f'Unknown style type: {style_type}',
                'available_types': list(css_templates.keys())
            }
        
        return {
            'status': 'success',
            'style_type': style_type,
            'css': css_templates[style_type],
            'usage': f'Copy this CSS to your stylesheet or <style> tag',
            'tailwind_compatible': True
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f'Failed to generate CSS: {str(e)}'
        }


def generate_apple_ui_component(component_type: str, options: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Generate Apple iOS 18 Liquid Glass UI components (React/JSX).
    
    Component Types:
    - "button" - Glass button with hover effects
    - "card" - Glass card container
    - "input" - Glass input field
    - "modal" - Full-screen glass modal
    - "navbar" - Glass navigation bar
    - "sidebar" - Glass sidebar menu
    - "hero" - Hero section with animated orbs
    
    Args:
        component_type: Type of component to generate
        options: Additional options (e.g., "with-icon" for buttons)
        tool_context: ADK tool context (optional)
        
    Returns:
        dict: Generated React component code
    """
    try:
        components = {
            "button": """import React from 'react';

export const GlassButton = ({ children, onClick, variant = 'primary' }) => {
  const baseStyles = "backdrop-blur-xl border border-white/20 rounded-2xl px-6 py-3 font-semibold transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl";
  
  const variants = {
    primary: "bg-gradient-to-r from-pink-500/20 to-purple-500/20 hover:from-pink-500/30 hover:to-purple-500/30 text-white",
    secondary: "bg-white/10 hover:bg-white/20 text-white",
    glass: "bg-black/40 hover:bg-black/50 text-white"
  };
  
  return (
    <button 
      onClick={onClick}
      className={`${baseStyles} ${variants[variant]}`}
    >
      {children}
    </button>
  );
};""",
            
            "card": """import React from 'react';

export const GlassCard = ({ children, className = '' }) => {
  return (
    <div className={`
      bg-black/60 backdrop-blur-2xl 
      border border-white/10 
      rounded-3xl p-6 
      transition-all duration-300 
      hover:-translate-y-2 hover:shadow-2xl hover:border-white/20
      ${className}
    `}>
      {children}
    </div>
  );
};""",
            
            "input": """import React from 'react';

export const GlassInput = ({ placeholder, value, onChange, type = 'text' }) => {
  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className="
        w-full px-4 py-3 
        bg-white/10 backdrop-blur-xl 
        border border-white/20 
        rounded-2xl 
        text-white placeholder-white/50 
        focus:outline-none focus:border-white/40 focus:bg-white/15
        transition-all duration-300
      "
    />
  );
};""",
            
            "modal": """import React from 'react';

export const GlassModal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="
        relative z-10 w-full max-w-lg
        bg-black/80 backdrop-blur-2xl 
        border border-white/20 
        rounded-3xl p-8 
        shadow-2xl
      ">
        {children}
      </div>
    </div>
  );
};""",
            
            "navbar": """import React from 'react';

export const GlassNavbar = ({ logo, links }) => {
  return (
    <nav className="
      sticky top-0 z-50 
      bg-black/80 backdrop-blur-2xl 
      border-b border-white/10 
      px-8 py-4
    ">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="text-2xl font-bold text-white">{logo}</div>
        
        <div className="flex gap-8">
          {links.map((link, i) => (
            <a 
              key={i}
              href={link.href}
              className="text-white/80 hover:text-white transition-colors"
            >
              {link.label}
            </a>
          ))}
        </div>
      </div>
    </nav>
  );
};""",
            
            "hero": """import React from 'react';

export const GlassHero = ({ title, subtitle, cta }) => {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-black">
      {/* Animated Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-pink-500 rounded-full blur-3xl opacity-30 animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500 rounded-full blur-3xl opacity-30 animate-pulse" style={{animationDelay: '1s'}} />
      <div className="absolute top-1/2 right-1/3 w-96 h-96 bg-cyan-400 rounded-full blur-3xl opacity-20 animate-pulse" style={{animationDelay: '2s'}} />
      
      {/* Content */}
      <div className="relative z-10 text-center px-4">
        <h1 className="text-7xl font-bold text-white mb-6 bg-clip-text text-transparent bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-400">
          {title}
        </h1>
        <p className="text-2xl text-white/80 mb-8">{subtitle}</p>
        {cta}
      </div>
    </div>
  );
};"""
        }
        
        if component_type not in components:
            return {
                'status': 'error',
                'error': f'Unknown component type: {component_type}',
                'available_types': list(components.keys())
            }
        
        return {
            'status': 'success',
            'component_type': component_type,
            'code': components[component_type],
            'framework': 'React + Tailwind CSS',
            'usage': 'Save as a .jsx or .tsx file and import into your app',
            'dependencies': ['react', 'tailwindcss']
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f'Failed to generate component: {str(e)}'
        }


def write_file_simple(file_path: str, content: str, tool_context: ToolContext) -> dict:
    """
    Write content to a file on the REAL file system (persistent).
    
    Use this to create project files like package.json, index.html, App.tsx, etc.
    
    Args:
        file_path: Path where to write the file (e.g., "./my-project/package.json")
        content: The file content to write
        
    Returns:
        dict with 'status', 'file_path', and 'message'
    """
    import os
    
    try:
        # Convert to absolute path
        abs_path = os.path.abspath(file_path)
        
        # Ensure parent directory exists
        parent_dir = os.path.dirname(abs_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        
        # Write the file
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            'status': 'success',
            'file_path': abs_path,
            'message': f'File written: {abs_path}'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }


def read_file_content(filepath: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Read a file and return its contents.
    
    Args:
        filepath: Path to the file to read
        tool_context: ADK tool context (optional)
        
    Returns:
        dict: File contents and metadata
    """
    try:
        path = Path(filepath)
        
        if not path.exists():
            return {
                'status': 'error',
                'error': f'File not found: {filepath}'
            }
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'status': 'success',
            'filepath': str(path.absolute()),
            'content': content,
            'size_bytes': len(content),
            'lines': len(content.split('\n'))
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f'Failed to read file: {str(e)}'
        }

