import requests
import json
import time

# Wait for server to start
time.sleep(2)

def test_covid_symptoms():
    url = "http://127.0.0.1:8000/consult"
    
    # Test 1: Common COVID symptoms
    print("=== Test 1: fever, cough, fatigue ===")
    data = {"symptoms": ["fever", "cough", "fatigue"]}
    try:
        response = requests.post(url, json=data)
        result = response.json()
        print(f"Result: {result['source']} - {result['result'].get('disease', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Exact COVID symptoms
    print("\n=== Test 2: fever or chills, cough ===")
    data = {"symptoms": ["fever or chills", "cough"]}
    try:
        response = requests.post(url, json=data)
        result = response.json()
        print(f"Result: {result['source']} - {result['result'].get('disease', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: COVID-specific symptoms
    print("\n=== Test 3: loss of taste or smell, shortness of breath ===")
    data = {"symptoms": ["loss of taste or smell", "shortness of breath"]}
    try:
        response = requests.post(url, json=data)
        result = response.json()
        print(f"Result: {result['source']} - {result['result'].get('disease', 'N/A')}")
        if result['source'] == 'dataset':
            print(f"Medicines: {', '.join(result['result']['medicines'][:2])}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_covid_symptoms()