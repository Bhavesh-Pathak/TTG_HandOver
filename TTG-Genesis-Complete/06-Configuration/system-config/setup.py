#!/usr/bin/env python3
"""
TTG Genesis Setup Script
Automated setup for the Text-to-Game world generation system
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🎮 TTG Genesis - Text to Game World Generator")
    print("🚀 Setup Script for Unreal Engine 5 Integration")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    print("\n🤖 Checking Ollama installation...")
    
    try:
        # Check if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        
        models = response.json().get("models", [])
        print("✅ Ollama is running")
        print(f"📦 Available models: {[m['name'] for m in models]}")
        
        # Check for recommended models
        model_names = [m['name'] for m in models]
        recommended = ["llama2", "llama3", "mistral"]
        
        has_recommended = any(any(rec in name for rec in recommended) for name in model_names)
        
        if not has_recommended:
            print("\n💡 Recommended: Install a language model")
            print("   Run: ollama pull llama2")
            print("   Or:  ollama pull llama3")
        
        return True
        
    except requests.exceptions.RequestException:
        print("❌ Ollama is not running or not installed")
        print("\n💡 To install Ollama:")
        print("   1. Visit: https://ollama.ai")
        print("   2. Download and install Ollama")
        print("   3. Run: ollama serve")
        print("   4. Run: ollama pull llama2")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "ue5_exports",
        "ttg-genesis/logs",
        "ttg-genesis/templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

def test_system():
    """Test the system with a simple prompt"""
    print("\n🧪 Testing system...")
    
    try:
        # Import and test the prompt parser
        sys.path.append("ttg-genesis/bhiv-core")
        from prompt_parser import create_world_from_prompt, validate_ollama_connection
        
        # Test Ollama connection
        if validate_ollama_connection():
            print("✅ Ollama connection test passed")
        else:
            print("⚠️  Ollama not available, will use fallback mode")
        
        # Test world generation
        test_prompt = "Create a small forest clearing with a friendly NPC"
        print(f"\n🎯 Testing with prompt: {test_prompt}")
        
        result = create_world_from_prompt(test_prompt)
        if result:
            print("✅ World generation test passed")
            return True
        else:
            print("❌ World generation test failed")
            return False
            
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Continuing without all dependencies...")
    
    # Create directories
    create_directories()
    
    # Check Ollama
    ollama_available = check_ollama_installation()
    
    # Test system
    print("\n" + "=" * 60)
    if test_system():
        print("\n🎉 Setup completed successfully!")
        
        if ollama_available:
            print("\n🚀 You're ready to generate game worlds!")
        else:
            print("\n⚠️  Setup complete, but Ollama is not available.")
            print("   The system will work in fallback mode.")
        
        print("\n📖 Usage:")
        print("   python ttg-genesis/bhiv-core/prompt-parser.py")
        print('   python ttg-genesis/bhiv-core/prompt-parser.py "Your prompt here"')
        
    else:
        print("\n❌ Setup completed with issues.")
        print("   Check the error messages above and try again.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
