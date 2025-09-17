#!/usr/bin/env python3
import subprocess
import sys
import time
import requests
import webbrowser
import os

def check_python():
    print("✓ Python version:", sys.version)

def install_requirements():
    print("Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/app_backend/requirements.txt"], check=True)

def start_server():
    print("Starting server...")
    os.chdir("backend/app_backend")
    subprocess.Popen([sys.executable, "run.py"])
    time.sleep(3)

def test_api():
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        print("✓ Server health:", response.json())
        
        response = requests.post("http://127.0.0.1:8000/consult", 
                               json={"symptoms": ["fever", "cough"]})
        print("✓ API test:", response.json())
        return True
    except Exception as e:
        print("✗ API test failed:", e)
        return False

def open_frontend():
    frontend_path = os.path.abspath("frontend/mobile/index.html")
    print(f"Opening frontend: {frontend_path}")
    webbrowser.open(f"file://{frontend_path}")

if __name__ == "__main__":
    try:
        check_python()
        install_requirements()
        start_server()
        if test_api():
            open_frontend()
            print("\n🎉 Application started successfully!")
            print("Backend: http://127.0.0.1:8000")
            print("Frontend: opened in browser")
        else:
            print("❌ Failed to start application")
    except Exception as e:
        print(f"❌ Error: {e}")