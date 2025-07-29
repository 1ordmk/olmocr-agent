#!/usr/bin/env python3
"""
Setup script for OLMoCR Streamlit App
This script will install all necessary dependencies and set up the environment.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"\n{'='*50}")
    print(f"🔧 {description}")
    print(f"Running: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_system_dependencies():
    """Install system-level dependencies based on OS"""
    system = platform.system().lower()
    
    if system == "linux":
        print("🐧 Detected Linux system")
        # Ubuntu/Debian dependencies for PDF processing
        commands = [
            "sudo apt-get update",
            "sudo apt-get install -y poppler-utils",
            "sudo apt-get install -y tesseract-ocr",
            "sudo apt-get install -y tesseract-ocr-eng",
            "sudo apt-get install -y libtesseract-dev",
            "sudo apt-get install -y libleptonica-dev",
            "sudo apt-get install -y pkg-config"
        ]
        
        for cmd in commands:
            if not run_command(cmd, f"Installing system dependency: {cmd.split()[-1]}"):
                print(f"⚠️  Warning: Failed to install {cmd.split()[-1]}")
                
    elif system == "darwin":  # macOS
        print("🍎 Detected macOS system")
        # Check if Homebrew is installed
        if run_command("which brew", "Checking for Homebrew"):
            commands = [
                "brew install poppler",
                "brew install tesseract",
                "brew install pkg-config"
            ]
            
            for cmd in commands:
                if not run_command(cmd, f"Installing: {cmd.split()[-1]}"):
                    print(f"⚠️  Warning: Failed to install {cmd.split()[-1]}")
        else:
            print("⚠️  Homebrew not found. Please install Homebrew first:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            
    elif system == "windows":
        print("🪟 Detected Windows system")
        print("⚠️  For Windows, you may need to manually install:")
        print("   - Poppler: https://poppler.freedesktop.org/")
        print("   - Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - Add them to your PATH environment variable")
    
    return True

def create_virtual_environment():
    """Create a virtual environment for the project"""
    venv_name = "olmocr_env"
    
    if os.path.exists(venv_name):
        print(f"📁 Virtual environment '{venv_name}' already exists")
        return venv_name
    
    if run_command(f"python -m venv {venv_name}", f"Creating virtual environment: {venv_name}"):
        print(f"✅ Virtual environment '{venv_name}' created successfully")
        return venv_name
    else:
        print("❌ Failed to create virtual environment")
        return None

def activate_and_install_packages(venv_name):
    """Activate virtual environment and install Python packages"""
    system = platform.system().lower()
    
    if system == "windows":
        activate_cmd = f"{venv_name}\\Scripts\\activate"
        pip_cmd = f"{venv_name}\\Scripts\\pip"
    else:
        activate_cmd = f"source {venv_name}/bin/activate"
        pip_cmd = f"{venv_name}/bin/pip"
    
    # Upgrade pip first
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        print("⚠️  Warning: Failed to upgrade pip")
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python packages"):
        print("❌ Failed to install requirements")
        return False
    
    print("✅ All Python packages installed successfully!")
    return True

def create_startup_script(venv_name):
    """Create a startup script to run the app"""
    system = platform.system().lower()
    
    if system == "windows":
        script_name = "run_app.bat"
        script_content = f"""@echo off
echo Starting OLMoCR Streamlit App...
call {venv_name}\\Scripts\\activate
streamlit run olmocr_app.py
pause
"""
    else:
        script_name = "run_app.sh"
        script_content = f"""#!/bin/bash
echo "Starting OLMoCR Streamlit App..."
source {venv_name}/bin/activate
streamlit run olmocr_app.py
"""
    
    with open(script_name, 'w') as f:
        f.write(script_content)
    
    if system != "windows":
        run_command(f"chmod +x {script_name}", f"Making {script_name} executable")
    
    print(f"✅ Startup script created: {script_name}")
    return script_name

def main():
    """Main setup function"""
    print("🚀 OLMoCR Streamlit App Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install system dependencies
    print("\n📦 Installing system dependencies...")
    install_system_dependencies()
    
    # Create virtual environment
    print("\n🔧 Setting up Python environment...")
    venv_name = create_virtual_environment()
    if not venv_name:
        print("❌ Setup failed: Could not create virtual environment")
        sys.exit(1)
    
    # Install Python packages
    print("\n📚 Installing Python packages...")
    if not activate_and_install_packages(venv_name):
        print("❌ Setup failed: Could not install Python packages")
        sys.exit(1)
    
    # Create startup script
    print("\n📝 Creating startup script...")
    script_name = create_startup_script(venv_name)
    
    # Final instructions
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\n📋 Next steps:")
    print("1. Make sure olmocr_app.py is in the current directory")
    print("2. Run the app using one of these methods:")
    print(f"   • Double-click: {script_name}")
    
    if platform.system().lower() == "windows":
        print(f"   • Command line: {script_name}")
    else:
        print(f"   • Command line: ./{script_name}")
        print(f"   • Manual: source {venv_name}/bin/activate && streamlit run olmocr_app.py")
    
    print("\n🌐 The app will open in your web browser at http://localhost:8501")
    print("\n📖 For more information, visit: https://github.com/allenai/olmocr")

if __name__ == "__main__":
    main()
