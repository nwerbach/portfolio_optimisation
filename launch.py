#!/usr/bin/env python3
"""
Portfolio Optimizer - Universal Launcher
Works on Windows, Mac, and Linux
"""

import sys
import subprocess
import os


def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True


def install_dependencies():
    """Install required dependencies"""
    try:
        import pulp
        import pandas
        import openpyxl
        print("✓ All dependencies are installed")
        return True
    except ImportError:
        print("Installing required dependencies...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✓ Dependencies installed successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to install dependencies: {e}")
            return False


def launch_application():
    """Launch the Portfolio Optimizer application"""
    print("\nLaunching Portfolio Optimizer Advanced...")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "portfolio_optimizer_advanced.py"], check=False)
        return True
    except Exception as e:
        print(f"✗ Error launching application: {e}")
        return False


def main():
    """Main launcher function"""
    print("=" * 50)
    print("Portfolio Optimizer Pro - Launcher")
    print("=" * 50)
    print()
    
    # Check Python version
    print("Checking Python version...")
    if not check_python_version():
        return 1
    print(f"✓ Python {sys.version.split()[0]}")
    print()
    
    # Check and install dependencies
    print("Checking dependencies...")
    if not install_dependencies():
        return 1
    print()
    
    # Launch application
    if not launch_application():
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
