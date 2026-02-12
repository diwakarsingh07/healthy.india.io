import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load complete health dataset
with open("health_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare training data
diseases = []
all_text = []

for disease in data["diseases"]:
    diseases.append(disease["name"])
    
    # Combine all disease info into training text
    text_parts = []
    text_parts.extend(disease["symptoms"])
    text_parts.extend(disease["medicines"])
    text_parts.extend(disease.get("prevention", []))
    text_parts.extend(disease.get("home_care", []))
    text_parts.append(disease["description"])
    
    combined_text = " ".join(text_parts).lower()
    all_text.append(combined_text)

# Train advanced model
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 3),
    max_features=5000,
    min_df=1,
    max_df=0.8
)

tfidf_matrix = vectorizer.fit_transform(all_text)

# Save trained model
model_data = {
    'vectorizer': vectorizer,
    'tfidf_matrix': tfidf_matrix,
    'diseases': diseases,
    'disease_data': {d["name"]: d for d in data["diseases"]}
}

with open("trained_model.pkl", "wb") as f:
    pickle.dump(model_data, f)

print(f"Trained model with {len(diseases)} diseases")
print("Model saved to trained_model.pkl")