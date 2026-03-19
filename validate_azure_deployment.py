#!/usr/bin/env python3
"""
Azure Deployment Validation Script
Checks all requirements for successful Azure deployment
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(check_name, passed, message=""):
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} | {check_name}")
    if message:
        print(f"       {message}")

def check_file_exists(filename):
    """Check if file exists"""
    exists = os.path.isfile(filename)
    print_status(f"File exists: {filename}", exists)
    return exists

def check_python_version():
    """Check Python version (3.9+)"""
    version = sys.version_info
    is_valid = version.major >= 3 and version.minor >= 9
    print_status(f"Python version >= 3.9", is_valid, f"Current: {version.major}.{version.minor}")
    return is_valid

def check_streamlit_installed():
    """Check if Streamlit is installed"""
    try:
        result = subprocess.run(['streamlit', '--version'], capture_output=True, text=True)
        installed = result.returncode == 0
        print_status("Streamlit installed", installed, result.stdout.strip())
        return installed
    except FileNotFoundError:
        print_status("Streamlit installed", False, "Not found in PATH")
        return False

def check_requirements_txt():
    """Check requirements.txt content"""
    if not os.path.isfile('requirements.txt'):
        print_status("requirements.txt content", False, "File not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required_packages = ['pandas', 'numpy', 'streamlit']
    found_packages = all(pkg in content for pkg in required_packages)
    
    print_status("requirements.txt has required packages", found_packages)
    return found_packages

def check_streamlit_app():
    """Check if streamlit_app.py exists and is valid"""
    if not os.path.isfile('streamlit_app.py'):
        print_status("streamlit_app.py exists", False)
        return False
    
    print_status("streamlit_app.py exists", True)
    
    # Check if it's valid Python
    try:
        with open('streamlit_app.py', 'r') as f:
            compile(f.read(), 'streamlit_app.py', 'exec')
        print_status("streamlit_app.py is valid Python", True)
        return True
    except SyntaxError as e:
        print_status("streamlit_app.py is valid Python", False, str(e))
        return False

def check_startup_script():
    """Check if startup.sh exists and is executable"""
    if not os.path.isfile('startup.sh'):
        print_status("startup.sh exists", False)
        return False
    
    print_status("startup.sh exists", True)
    
    # Check if executable
    is_executable = os.access('startup.sh', os.X_OK)
    print_status("startup.sh is executable", is_executable)
    
    if not is_executable:
        print(f"       {Colors.YELLOW}Run: chmod +x startup.sh{Colors.END}")
    
    return True

def check_web_config():
    """Check if web.config exists"""
    exists = os.path.isfile('web.config')
    print_status("web.config exists", exists)
    return exists

def check_github_workflow():
    """Check if GitHub Actions workflow exists"""
    workflow_path = '.github/workflows/deploy.yml'
    exists = os.path.isfile(workflow_path)
    print_status(f"GitHub Actions workflow exists", exists)
    return exists

def check_git_configured():
    """Check if git is configured"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        is_git_repo = result.returncode == 0
        print_status("Git repository initialized", is_git_repo)
        return is_git_repo
    except FileNotFoundError:
        print_status("Git repository initialized", False, "Git not found")
        return False

def check_git_remote():
    """Check if git remote is configured"""
    try:
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        has_remote = 'github.com' in result.stdout or 'origin' in result.stdout
        print_status("Git remote configured", has_remote)
        if has_remote:
            print(f"       Remote: {result.stdout.strip().split()[0]}")
        return has_remote
    except:
        print_status("Git remote configured", False)
        return False

def check_directory_structure():
    """Check if directory structure is correct"""
    dirs_to_check = [
        '.git',
        '.github/workflows',
    ]
    
    all_exist = True
    for dir_path in dirs_to_check:
        exists = os.path.isdir(dir_path)
        all_exist = all_exist and exists
        print_status(f"Directory exists: {dir_path}", exists)
    
    return all_exist

def main():
    """Run all validation checks"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Azure Deployment Validation Script{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}🔍 Checking Environment...{Colors.END}\n")
    
    checks = [
        ("Python Version", check_python_version()),
        ("Streamlit Installed", check_streamlit_installed()),
        ("File Existence Checks", True),  # Header
    ]
    
    print(f"\n{Colors.YELLOW}📁 Checking Files...{Colors.END}\n")
    
    files_ok = (
        check_file_exists('streamlit_app.py') and
        check_file_exists('requirements.txt') and
        check_file_exists('startup.sh') and
        check_file_exists('web.config')
    )
    
    print(f"\n{Colors.YELLOW}📝 Checking File Contents...{Colors.END}\n")
    
    content_ok = (
        check_requirements_txt() and
        check_streamlit_app() and
        check_startup_script() and
        check_web_config()
    )
    
    print(f"\n{Colors.YELLOW}🔗 Checking Git Configuration...{Colors.END}\n")
    
    git_ok = (
        check_git_configured() and
        check_git_remote()
    )
    
    print(f"\n{Colors.YELLOW}📂 Checking Directory Structure...{Colors.END}\n")
    
    dir_ok = (
        check_directory_structure() and
        check_github_workflow()
    )
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Validation Summary{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    all_ok = files_ok and content_ok and git_ok and dir_ok
    
    if all_ok:
        print(f"{Colors.GREEN}✅ All checks passed!{Colors.END}")
        print(f"\n{Colors.GREEN}You're ready to deploy!{Colors.END}")
        print(f"\nNext steps:")
        print(f"1. git add .")
        print(f"2. git commit -m 'Deploy to Azure'")
        print(f"3. git push origin main")
        return 0
    else:
        print(f"{Colors.RED}❌ Some checks failed!{Colors.END}")
        print(f"\n{Colors.YELLOW}Fix the issues above before deploying.{Colors.END}")
        print(f"\nCommon fixes:")
        print(f"- Make startup.sh executable: chmod +x startup.sh")
        print(f"- Ensure requirements.txt has all dependencies")
        print(f"- Verify streamlit_app.py syntax")
        print(f"- Check git is configured and has remote")
        return 1

if __name__ == '__main__':
    sys.exit(main())
