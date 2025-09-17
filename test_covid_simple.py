import requests
import json

def test_covid():
    url = "http://127.0.0.1:8000/consult"
    
    tests = [
        ["fever", "cough", "fatigue"],
        ["loss of taste", "shortness of breath"],
        ["covid symptoms"],
        ["fever or chills", "cough"]
    ]
    
    for symptoms in tests:
        print(f"Testing: {symptoms}")
        try:
            response = requests.post(url, json={"symptoms": symptoms})
            result = response.json()
            
            if result["source"] == "dataset":
                print(f"  Result: {result['result']['disease']}")
            else:
                print(f"  No match: {result['result']['response']}")
        except Exception as e:
            print(f"  Error: {e}")
        print()

if __name__ == "__main__":
    test_covid()