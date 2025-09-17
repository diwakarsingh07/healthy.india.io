import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load complete health dataset
with open("backend/health_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare training data with keywords
diseases = []
all_text = []
disease_keywords = {}

for disease in data["diseases"]:
    disease_name = disease["name"]
    diseases.append(disease_name)
    
    # Create keyword variations for direct disease name matching
    keywords = [
        disease_name.lower(),
        disease_name.lower().replace(" ", ""),
        disease_name.lower().replace("-", ""),
        disease_name.lower().replace("(", "").replace(")", "")
    ]
    
    # Add common abbreviations
    if "COVID-19" in disease_name:
        keywords.extend(["covid", "corona", "coronavirus", "covid19", "covid-19"])
    elif "Common Cold" in disease_name:
        keywords.extend(["cold", "flu symptoms"])
    elif "Influenza" in disease_name:
        keywords.extend(["flu", "influenza"])
    elif "UTI" in disease_name or "Urinary Tract" in disease_name:
        keywords.extend(["uti", "urinary infection"])
    elif "Strep Throat" in disease_name:
        keywords.extend(["strep", "throat infection"])
    elif "Pneumonia" in disease_name:
        keywords.extend(["pneumonia", "lung infection"])
    elif "Diabetes" in disease_name:
        keywords.extend(["diabetes", "sugar", "blood sugar"])
    elif "Hypertension" in disease_name:
        keywords.extend(["high blood pressure", "bp", "hypertension"])
    elif "Heart Attack" in disease_name:
        keywords.extend(["heart attack", "cardiac arrest", "mi"])
    elif "Asthma" in disease_name:
        keywords.extend(["asthma", "breathing problem"])
    
    disease_keywords[disease_name] = keywords
    
    # Combine all text for training
    text_parts = keywords.copy()
    text_parts.extend(disease["symptoms"])
    text_parts.extend(disease["medicines"])
    text_parts.extend(disease.get("prevention", []))
    text_parts.extend(disease.get("home_care", []))
    text_parts.append(disease["description"])
    
    combined_text = " ".join(text_parts).lower()
    all_text.append(combined_text)

# Train model
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 3),
    max_features=10000,
    min_df=1
)

tfidf_matrix = vectorizer.fit_transform(all_text)

# Save model with keywords
model_data = {
    'vectorizer': vectorizer,
    'tfidf_matrix': tfidf_matrix,
    'diseases': diseases,
    'disease_data': {d["name"]: d for d in data["diseases"]},
    'disease_keywords': disease_keywords
}

with open("backend/app_backend/trained_model.pkl", "wb") as f:
    pickle.dump(model_data, f)

print(f"Trained model with {len(diseases)} diseases and keywords")
print("Keywords added for direct disease name matching")