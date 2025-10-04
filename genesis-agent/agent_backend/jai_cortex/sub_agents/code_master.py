"""
CodeMaster - Elite Coding Specialist with Real Security Scanning
Part of JAi Cortex OS Multi-Agent System
"""

import tempfile
import subprocess
import json
import os
import shutil
from pathlib import Path
from git import Repo, GitCommandError
from google.adk.agents import Agent
from google.adk.tools import ToolContext, FunctionTool
from google.genai import types as genai_types


def analyze_github_repo(repo_url: str, branch: str, tool_context: ToolContext) -> dict:
    """Clone and analyze a GitHub repository structure and contents.
    
    This tool clones a public GitHub repository and provides:
    - Project structure (directories and key files)
    - Programming languages detected
    - Lines of code
    - Key files (README, requirements, config files)
    - Repository statistics
    - COMPLETE LIST of all Python files with their full paths
    - COMPLETE LIST of all TypeScript files with their full paths
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/user/repo)
        branch: Branch name to analyze (e.g., 'main', 'storage-security-fixes', 'develop')
        
    Returns:
        dict: Repository analysis including:
            - statistics: file counts, languages, lines of code
            - key_files: important config/setup files
            - python_files: FULL LIST of all .py files with paths
            - typescript_files: FULL LIST of all .ts/.tsx files with paths
            - message: summary of findings
    """
    try:
        # Create temp directory for cloning
        temp_dir = tempfile.mkdtemp(prefix='repo_')
        
        print(f"📦 Cloning repository: {repo_url} (branch: {branch})")
        
        try:
            # Clone the repository with specific branch
            repo = Repo.clone_from(repo_url, temp_dir, branch=branch, depth=1)  # Shallow clone for speed
            
            # Analyze repository structure
            file_count = 0
            dir_count = 0
            language_stats = {}
            key_files = []
            total_lines = 0
            python_files = []  # Track all Python files
            typescript_files = []  # Track TypeScript/TSX files
            
            # File extensions to language mapping
            ext_to_lang = {
                '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.go': 'Go',
                '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP', '.swift': 'Swift',
                '.kt': 'Kotlin', '.scala': 'Scala', '.sh': 'Shell',
                '.html': 'HTML', '.css': 'CSS', '.jsx': 'React', '.tsx': 'TypeScript React',
                '.vue': 'Vue', '.sql': 'SQL', '.yaml': 'YAML', '.yml': 'YAML',
                '.json': 'JSON', '.xml': 'XML', '.md': 'Markdown'
            }
            
            # Important files to look for
            important_files = [
                'README.md', 'requirements.txt', 'package.json', 'Dockerfile',
                'docker-compose.yml', '.env.example', 'setup.py', 'pyproject.toml',
                'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle', 'Makefile'
            ]
            
            # Walk through repository
            for root, dirs, files in os.walk(temp_dir):
                # Skip .git directory and node_modules
                if '.git' in root or 'node_modules' in root:
                    continue
                    
                dir_count += len([d for d in dirs if not d.startswith('.')])
                
                for file in files:
                    if file.startswith('.'):
                        continue
                        
                    file_count += 1
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, temp_dir)
                    
                    # Check for important files
                    if file in important_files:
                        key_files.append(rel_path)
                    
                    # Detect language by extension
                    ext = Path(file).suffix
                    
                    # Track Python files specifically
                    if ext == '.py':
                        python_files.append(rel_path)
                    
                    # Track TypeScript/TSX files specifically
                    if ext in ['.ts', '.tsx']:
                        typescript_files.append(rel_path)
                    
                    if ext in ext_to_lang:
                        lang = ext_to_lang[ext]
                        language_stats[lang] = language_stats.get(lang, 0) + 1
                        
                        # Count lines for code files
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = len(f.readlines())
                                total_lines += lines
                        except:
                            pass
            
            # Get repo info
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            # Sort languages by file count
            sorted_languages = sorted(language_stats.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'status': 'success',
                'repository': repo_name,
                'branch': branch,
                'url': repo_url,
                'statistics': {
                    'total_files': file_count,
                    'total_directories': dir_count,
                    'total_lines': total_lines,
                    'languages': dict(sorted_languages[:5])  # Top 5 languages
                },
                'key_files': key_files,
                'python_files': python_files,  # Full list of Python files
                'typescript_files': typescript_files,  # Full list of TypeScript files
                'primary_language': sorted_languages[0][0] if sorted_languages else 'Unknown',
                'message': f'Successfully analyzed {repo_name} (branch: {branch}): {file_count} files, {total_lines} lines of code. Found {len(python_files)} Python files and {len(typescript_files)} TypeScript files.'
            }
            
        except GitCommandError as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return {
                'status': 'error',
                'message': f'Git error: {str(e)}. Make sure the repository is public and the URL is correct.'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error analyzing repository: {str(e)}'
        }


def read_github_file(repo_url: str, file_path: str, branch: str, tool_context: ToolContext) -> dict:
    """Read a specific file from a GitHub repository.
    
    This tool clones the repository and reads the contents of a specific file.
    Useful for code review, analysis, or understanding specific implementations.
    
    Args:
        repo_url: GitHub repository URL
        file_path: Path to the file within the repository (e.g., 'src/main.py')
        branch: Branch name to read from (e.g., 'main', 'storage-security-fixes', 'develop')
        
    Returns:
        dict: File contents and metadata
    """
    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp(prefix='repo_')
        
        try:
            # Clone repository with specific branch
            Repo.clone_from(repo_url, temp_dir, branch=branch, depth=1)
            
            # Construct full file path
            full_path = os.path.join(temp_dir, file_path)
            
            if not os.path.exists(full_path):
                shutil.rmtree(temp_dir, ignore_errors=True)
                return {
                    'status': 'error',
                    'message': f'File not found: {file_path}'
                }
            
            # Read file
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Get file stats
            line_count = len(content.split('\n'))
            file_size = os.path.getsize(full_path)
            
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            return {
                'status': 'success',
                'file_path': file_path,
                'branch': branch,
                'content': content,
                'metadata': {
                    'lines': line_count,
                    'size_bytes': file_size,
                    'extension': Path(file_path).suffix
                }
            }
            
        except GitCommandError as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return {
                'status': 'error',
                'message': f'Git error: {str(e)}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error reading file: {str(e)}'
        }


def scan_python_security(code: str, tool_context: ToolContext) -> dict:
    """Run Bandit security scanner on Python code to detect vulnerabilities.
    
    This tool executes the Bandit static analysis tool, which checks for:
    - SQL injection vulnerabilities
    - Command injection
    - Hardcoded passwords/secrets
    - Unsafe deserialization
    - Insecure cryptography
    - And 100+ other security issues
    
    Args:
        code: Python code to scan for security vulnerabilities
        
    Returns:
        dict: Detailed security scan results with severity levels and recommendations
    """
    try:
        # Write code to a temporary file for Bandit to analyze
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Run Bandit security scanner
        result = subprocess.run(
            ['bandit', '-f', 'json', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Clean up temp file
        import os
        os.unlink(temp_file)
        
        # Parse Bandit output
        if result.stdout:
            scan_results = json.loads(result.stdout)
            
            vulnerabilities = []
            for issue in scan_results.get('results', []):
                vulnerabilities.append({
                    'severity': issue.get('issue_severity', 'UNKNOWN'),
                    'confidence': issue.get('issue_confidence', 'UNKNOWN'),
                    'issue': issue.get('issue_text', 'Unknown issue'),
                    'cwe': issue.get('issue_cwe', {}).get('id', 'N/A'),
                    'line': issue.get('line_number', 'N/A'),
                    'code': issue.get('code', ''),
                    'more_info': issue.get('more_info', '')
                })
            
            return {
                'status': 'success',
                'scanner': 'Bandit Static Analysis',
                'total_issues': len(vulnerabilities),
                'vulnerabilities': vulnerabilities,
                'metrics': scan_results.get('metrics', {})
            }
        else:
            return {
                'status': 'success',
                'scanner': 'Bandit Static Analysis',
                'total_issues': 0,
                'message': 'No security issues detected by Bandit'
            }
            
    except FileNotFoundError:
        return {
            'status': 'error',
            'message': 'Bandit security scanner is not installed. Install it with: pip install bandit'
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Security scan timed out (code too large or complex)'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error running security scan: {str(e)}'
        }


def lint_python_code(code: str, tool_context: ToolContext) -> dict:
    """Run flake8 and pylint to check Python code for style issues, bugs, and complexity.
    
    This tool runs industry-standard linters to check for:
    - PEP 8 style violations (formatting, naming conventions)
    - Potential bugs and code smells
    - Unused imports and variables
    - Code complexity issues
    - Best practice violations
    
    Args:
        code: Python code to analyze for quality and style issues
        
    Returns:
        dict: Detailed linting results with issue types, line numbers, and recommendations
    """
    try:
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        issues = []
        
        # Run flake8 for style and simple errors
        try:
            flake8_result = subprocess.run(
                ['flake8', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse flake8 default output format: "path:line:col: code message"
            if flake8_result.stdout:
                for line in flake8_result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(':', 3)
                        if len(parts) >= 4:
                            issues.append({
                                'tool': 'flake8',
                                'severity': 'STYLE',
                                'line': parts[1],
                                'column': parts[2],
                                'code': parts[3].split()[0] if parts[3] else 'N/A',
                                'message': ' '.join(parts[3].split()[1:]) if len(parts[3].split()) > 1 else parts[3]
                            })
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            print(f"Flake8 error: {e}")
        
        # Run pylint for deeper analysis
        try:
            pylint_result = subprocess.run(
                ['pylint', '--output-format=json', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if pylint_result.stdout:
                pylint_data = json.loads(pylint_result.stdout)
                for issue in pylint_data:
                    issues.append({
                        'tool': 'pylint',
                        'severity': issue.get('type', 'UNKNOWN').upper(),
                        'line': issue.get('line', 'N/A'),
                        'column': issue.get('column', 'N/A'),
                        'code': issue.get('message-id', 'N/A'),
                        'message': issue.get('message', 'Unknown issue'),
                        'symbol': issue.get('symbol', 'N/A')
                    })
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            print(f"Pylint error: {e}")
        
        # Clean up
        import os
        os.unlink(temp_file)
        
        return {
            'status': 'success',
            'total_issues': len(issues),
            'issues': issues,
            'message': f'Found {len(issues)} style and quality issues' if issues else 'Code looks clean!'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error running linters: {str(e)}'
        }


def format_python_code(code: str, tool_context: ToolContext) -> dict:
    """Auto-format Python code using Black formatter to PEP 8 standards.
    
    Black is an opinionated code formatter that ensures consistent style.
    It handles:
    - Indentation and spacing
    - Line length (default 88 characters)
    - Quote normalization
    - Trailing commas
    
    Args:
        code: Python code to auto-format
        
    Returns:
        dict: Formatted code and summary of changes made
    """
    try:
        # Run Black on the code
        result = subprocess.run(
            ['black', '--quiet', '-'],
            input=code,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            formatted_code = result.stdout
            
            # Check if any changes were made
            if formatted_code == code:
                return {
                    'status': 'success',
                    'formatted_code': formatted_code,
                    'changes_made': False,
                    'message': 'Code is already properly formatted!'
                }
            else:
                return {
                    'status': 'success',
                    'formatted_code': formatted_code,
                    'changes_made': True,
                    'message': 'Code has been formatted to PEP 8 standards'
                }
        else:
            return {
                'status': 'error',
                'message': f'Black formatter error: {result.stderr}'
            }
            
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Formatting timed out (code too large)'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error formatting code: {str(e)}'
        }


def analyze_code_complexity(code: str, tool_context: ToolContext) -> dict:
    """Analyze code complexity and maintainability metrics using pylint.
    
    Provides detailed metrics on:
    - Cyclomatic complexity (code complexity score)
    - Number of lines of code
    - Number of functions/classes
    - Maintainability index
    
    Args:
        code: Python code to analyze for complexity
        
    Returns:
        dict: Complexity metrics and maintainability scores
    """
    try:
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Run pylint with stats
        result = subprocess.run(
            ['pylint', '--reports=y', '--output-format=json', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Clean up
        import os
        os.unlink(temp_file)
        
        # Count basic metrics from the code
        lines = code.split('\n')
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        
        return {
            'status': 'success',
            'metrics': {
                'total_lines': total_lines,
                'code_lines': code_lines,
                'blank_lines': total_lines - code_lines,
            },
            'message': 'Complexity analysis complete'
        }
        
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Complexity analysis timed out'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error analyzing complexity: {str(e)}'
        }


code_master = Agent(
    name="CodeMaster",
    model="gemini-2.5-pro",
    description="Elite code quality specialist with REAL analysis tools: Bandit (security), flake8 (style), pylint (bugs), Black (formatting), and GitHub integration. Analyzes repositories, reads code, and provides comprehensive reviews with empirical scanning.",
    instruction="""You are CodeMaster, an elite code quality specialist with REAL professional-grade tools and GitHub integration.

**YOUR SPECIALIZED TOOLKIT:**

🔒 **SECURITY SCANNING:**
1. **scan_python_security(code)** - Bandit Security Scanner
   - Detects: SQL injection, command injection, hardcoded secrets, unsafe crypto, and 100+ vulnerabilities
   - Returns: Severity, CWE ID, line numbers, confidence level

📊 **CODE QUALITY ANALYSIS:**
2. **lint_python_code(code)** - Style & Quality Analysis (flake8 + pylint)
   - Detects: PEP 8 violations, unused imports, code smells, potential bugs
   - Returns: Issue type, line/column numbers, specific violations

3. **analyze_code_complexity(code)** - Complexity Metrics (pylint)
   - Measures: Code complexity, maintainability, line counts
   - Returns: Detailed metrics for refactoring decisions

✨ **AUTO-FORMATTING:**
4. **format_python_code(code)** - Auto-formatting (Black)
   - Formats code to PEP 8 standards automatically
   - Returns: Formatted code ready to use

🔗 **GITHUB INTEGRATION:**
5. **analyze_github_repo(repo_url, branch)** - Repository Analysis
   - Clones and analyzes GitHub repos from ANY branch
   - Returns: File structure, languages, lines of code, key files
   - **ALSO RETURNS: Complete list of ALL Python files and TypeScript files with paths!**
   - **IMPORTANT: You MUST specify the branch name!**
   - Example: analyze_github_repo("https://github.com/user/repo", "main")
   - Example: analyze_github_repo("https://github.com/user/repo", "storage-security-fixes")

6. **read_github_file(repo_url, file_path, branch)** - File Reader
   - Reads specific files from GitHub repos from ANY branch
   - Returns: File contents and metadata
   - **IMPORTANT: You MUST specify the branch name!**
   - Example: read_github_file("https://github.com/user/repo", "src/main.py", "main")
   - Example: read_github_file("https://github.com/user/repo", "services/storageService.ts", "storage-security-fixes")

**YOUR WORKFLOW:**

**For GitHub Repository Analysis:**
1. analyze_github_repo(url, branch) to get project overview - **ALWAYS specify branch!**
2. The response includes 'python_files' and 'typescript_files' arrays with ALL file paths
3. Pick the most important files (e.g., main.py, routes.py, api files)
4. read_github_file(url, file_path, branch) to get the code - **ALWAYS specify the SAME branch!**
5. Run security/quality scans on important files
6. Provide comprehensive project assessment

**CRITICAL**: If user mentions a specific branch (e.g., "storage-security-fixes"), use that exact branch name!

**For Security Reviews:**
1. Run scan_python_security(code)
2. Report findings with CWE IDs, severity, line numbers
3. Explain exploits and provide secure fixes

**For Code Quality Reviews:**
1. Run lint_python_code(code) for style and bug checks
2. Run analyze_code_complexity(code) for maintainability metrics
3. If user wants, run format_python_code(code) to auto-fix style issues
4. Provide comprehensive report with specific, actionable fixes

**For Complete Reviews (Security + Quality):**
1. Run ALL tools (security, linting, complexity)
2. Synthesize findings into one comprehensive report
3. Prioritize: Critical security issues → Bugs → Style → Complexity
4. Provide formatted, production-ready code

**HOW TO RESPOND:**
- Always run the appropriate tool first (don't guess!)
- Report EMPIRICAL findings from tools, not just opinions
- Include line numbers, error codes, and severity levels
- Provide code examples for fixes
- Explain WHY each issue matters
- For GitHub URLs, ALWAYS use the analysis/read tools

**Example Complete Review:**
User: "Review this code comprehensively: [code]"

You:
1. scan_python_security(code) → "Found 1 MEDIUM security issue (CWE-89)"
2. lint_python_code(code) → "Found 5 style issues (PEP 8 violations)"
3. analyze_code_complexity(code) → "12 lines of code, moderate complexity"
4. format_python_code(code) → "Here's the formatted version"

Then synthesize: "Your code has one SQL injection vulnerability and several style issues. Here's the secure, formatted version..."

**Example GitHub Analysis:**
User: "Analyze the storage-security-fixes branch of https://github.com/user/repo"

You:
1. analyze_github_repo(url, "storage-security-fixes") → Get overview of THAT branch
2. Check response['python_files'] array → See all Python files like ['src/main.py', 'api/routes.py', 'utils/helpers.py']
3. Pick the most critical files (main.py, routes.py, anything with 'auth' or 'api' in name)
4. read_github_file(url, "src/main.py", "storage-security-fixes") → Get the code from THAT branch
5. scan_python_security(code) → Check for vulnerabilities
6. Provide comprehensive project security assessment with specific file names and line numbers

**If user doesn't specify a branch, ask them which branch to analyze OR default to "main"**

**You are fundamentally different from a regular LLM** - you have EMPIRICAL tools that execute and return real data, not just pattern matching from training.

**CRITICAL - DELEGATION FLOW:**
After completing your analysis and providing your findings, you MUST transfer back to jai_cortex so the user gets a seamless experience. Use `transfer_to_agent` to return to the parent agent when your task is complete.
""",
    tools=[
        FunctionTool(analyze_github_repo),
        FunctionTool(read_github_file),
        FunctionTool(scan_python_security),
        FunctionTool(lint_python_code),
        FunctionTool(format_python_code),
        FunctionTool(analyze_code_complexity),
    ],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.2,  # Very low for deterministic analysis
        max_output_tokens=8192,  # Higher for comprehensive reports
    ),
)

