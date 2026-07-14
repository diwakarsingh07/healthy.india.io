import json
import os

# Load the dataset
DATASET_PATH = "health_dataset.json"
with open(DATASET_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
    DATASET = {}
    for disease in data.get("diseases", []):
        DATASET[disease["name"]] = {
            "symptoms": disease["symptoms"],
            "medicines": disease["medicines"],
            "advice": f"{disease['description']} {disease.get('note', '')}"
        }

def find_match_debug(symptoms):
    print(f"Input symptoms: {symptoms}")
    symptoms_lower = [s.lower().strip() for s in symptoms]
    print(f"Normalized input: {symptoms_lower}")
    
    best_match = None
    max_matches = 0
    
    for disease, details in DATASET.items():
        disease_symptoms = [s.lower() for s in details.get("symptoms", [])]
        matches = 0
        matched_symptoms = []
        
        for user_symptom in symptoms_lower:
            for disease_symptom in disease_symptoms:
                if user_symptom in disease_symptom or disease_symptom in user_symptom:
                    matches += 1
                    matched_symptoms.append(f"{user_symptom} -> {disease_symptom}")
                    break
        
        if matches > 0:
            print(f"\n{disease}: {matches} matches")
            print(f"  Disease symptoms: {disease_symptoms}")
            print(f"  Matched: {matched_symptoms}")
        
        if matches > max_matches:
            max_matches = matches
            best_match = {
                "disease": disease,
                "symptoms": details.get("symptoms", []),
                "medicines": details.get("medicines", []),
                "advice": details.get("advice", "")
            }
    
    print(f"\nBest match: {best_match['disease'] if best_match else 'None'} with {max_matches} matches")
    return best_match if max_matches > 0 else None

# Test COVID-19 symptoms
print("=== Testing COVID-19 symptoms ===")
covid_symptoms = ["fever", "cough", "fatigue"]
result = find_match_debug(covid_symptoms)

print("\n=== Testing exact COVID symptoms ===")
covid_exact = ["Fever or chills", "Cough"]
result = find_match_debug(covid_exact)

print("\n=== Testing shortness of breath ===")
breath_symptoms = ["shortness of breath"]
result = find_match_debug(breath_symptoms)