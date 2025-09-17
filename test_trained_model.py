import requests
import json
import time
import subprocess
import threading

def start_server():
    subprocess.run(["python", "backend/app_backend/run.py"])

def test_api():
    time.sleep(3)
    
    tests = [
        ["fever", "cough", "fatigue"],
        ["loss of taste", "shortness of breath"],
        ["fever or chills", "cough"],
        ["covid symptoms"],
        ["sore throat", "fever"],
        ["chest pain", "cough"]
    ]
    
    for symptoms in tests:
        print(f"Testing: {symptoms}")
        try:
            response = requests.post("http://127.0.0.1:8000/consult", 
                                   json={"symptoms": symptoms}, timeout=10)
            result = response.json()
            
            if result["source"] == "dataset":
                disease = result["result"]["disease"]
                confidence = result["result"].get("confidence", "N/A")
                print(f"  Result: {disease} (confidence: {confidence})")
            else:
                print(f"  Fallback: {result['source']}")
        except Exception as e:
            print(f"  Error: {e}")
        print()

if __name__ == "__main__":
    # Start server in background
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Test API
    test_api()