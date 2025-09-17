import requests
import json

# Test backend
try:
    # Test health endpoint
    response = requests.get("http://127.0.0.1:8000/health")
    print("Health check:", response.json())
    
    # Test consult endpoint
    data = {"symptoms": ["fever", "cough"]}
    response = requests.post("http://127.0.0.1:8000/consult", json=data)
    print("Consult result:", response.json())
    
except Exception as e:
    print("Error:", str(e))
    print("Backend is not running. Start it with: python backend/app_backend/run.py")