#!/usr/bin/env python3
import subprocess
import time
import requests
import json
import threading
import os

def start_backend():
    """Start the backend server"""
    os.chdir("backend/app_backend")
    subprocess.run(["python", "run.py"])

def test_api():
    """Test the API endpoints"""
    time.sleep(3)  # Wait for server to start
    
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get("http://127.0.0.1:8000/health")
        print("Health:", response.json())
        
        # Test consult endpoint
        print("\nTesting consult endpoint...")
        data = {"symptoms": ["fever", "cough"]}
        response = requests.post("http://127.0.0.1:8000/consult", json=data)
        result = response.json()
        print("Consult result:", json.dumps(result, indent=2))
        
        # Test with different symptoms
        print("\nTesting with headache...")
        data = {"symptoms": ["headache", "pressure"]}
        response = requests.post("http://127.0.0.1:8000/consult", json=data)
        result = response.json()
        print("Headache result:", json.dumps(result, indent=2))
        
    except Exception as e:
        print("Error testing API:", str(e))

if __name__ == "__main__":
    print("Starting backend server...")
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Test the API
    test_api()