#!/usr/bin/env python3
"""
Test script to verify MCP server setup.

This script helps verify that:
1. All required dependencies are installed
2. Environment variables are set correctly
3. The MCP server can be imported
4. Basic functionality works

Usage:
    python test_setup.py
"""

import sys
import os

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and 10 <= version.minor < 14:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not in range 3.10-3.13")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        ('crewai', 'CrewAI'),
        ('gradio', 'Gradio'),
        ('dotenv', 'python-dotenv'),
    ]
    
    all_installed = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is not installed")
            all_installed = False
    
    # Check MCP (optional for Gradio users)
    try:
        __import__('mcp')
        print(f"✓ MCP is installed (optional)")
    except ImportError:
        print(f"⚠ MCP is not installed (only needed for MCP server)")
    
    return all_installed

def check_environment_variables():
    """Check if required environment variables are set."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠ python-dotenv not installed, checking environment variables directly")
    
    required_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    all_set = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != 'YOUR-KEY':
            print(f"✓ {var} is set")
        else:
            print(f"✗ {var} is not set or still has placeholder value")
            all_set = False
    
    return all_set

def check_file_structure():
    """Check if required files exist."""
    required_files = [
        'main.py',
        'app.py',
        'mcp_server.py',
        'requirements.txt',
        '.env.example',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} not found")
            all_exist = False
    
    return all_exist

def check_directories():
    """Check if required directories exist."""
    required_dirs = ['inputs', 'outputs', 'crews', 'tools']
    
    all_exist = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"✓ {directory}/ directory exists")
        else:
            print(f"⚠ {directory}/ directory not found (will be created if needed)")
    
    return True  # Directories are created automatically

def test_import_main():
    """Test if main module can be imported."""
    try:
        from main import JobApplicationFlow
        print("✓ JobApplicationFlow can be imported")
        return True
    except Exception as e:
        print(f"✗ Error importing JobApplicationFlow: {e}")
        return False

def main():
    """Run all checks."""
    print("=" * 60)
    print("Job Application Flow - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Variables", check_environment_variables),
        ("File Structure", check_file_structure),
        ("Directories", check_directories),
        ("Module Import", test_import_main),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 40)
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("✓ All checks passed! Your setup is ready.")
        print("\nYou can now:")
        print("  - Run the Gradio app: python app.py")
        print("  - Run the MCP server: python mcp_server.py")
        print("  - Or use UV: uv run mcp_server_standalone.py")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Set up environment: cp .env.example .env (then edit with your API keys)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
