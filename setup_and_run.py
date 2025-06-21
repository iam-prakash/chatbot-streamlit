#!/usr/bin/env python3
"""
Setup and run script for Sixt Q&A Chatbot
"""

import subprocess
import sys
import os
import requests
import time

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        ('streamlit', 'streamlit'),
        ('fastapi', 'fastapi'), 
        ('uvicorn', 'uvicorn'),
        ('google-generativeai', 'google.generativeai'),
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4')
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)
    
    return len(missing_packages) == 0

def check_api_key():
    """Check if Google API key is set"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print("✅ GOOGLE_API_KEY is set")
        return True
    else:
        print("❌ GOOGLE_API_KEY not set")
        print("Please set it with: export GOOGLE_API_KEY='your-api-key'")
        return False

def start_backend():
    """Start the FastAPI backend"""
    print("\n🚀 Starting FastAPI backend...")
    
    # Check if backend is already running
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ Backend is already running")
            return True
    except:
        pass
    
    # Start backend in background
    try:
        backend_process = subprocess.Popen(
            [sys.executable, '-m', 'uvicorn', 'backend.app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
            cwd='.',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Check if it's running
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend started successfully")
                return True
        except:
            print("❌ Backend failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def main():
    print("🚗 Sixt Q&A Chatbot Setup")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependencies check failed")
        return
    
    # Check API key
    if not check_api_key():
        print("\n📝 Please get your API key from: https://makersuite.google.com/app/apikey")
        print("Then set it with: export GOOGLE_API_KEY='your-api-key'")
        return
    
    # Start backend
    if not start_backend():
        print("❌ Backend setup failed")
        return
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Make sure your API key is set: export GOOGLE_API_KEY='your-api-key'")
    print("2. Start the Streamlit app: streamlit run streamlit_app.py")
    print("3. Visit http://localhost:8501 for the chat interface")
    print("\n🔧 Alternative: Start backend manually with:")
    print("   cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main() 