import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load health dataset
with open("health_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare training data
diseases = []
symptoms_text = []

for disease in data["diseases"]:
    diseases.append(disease["name"])
    # Combine all symptoms into one text
    symptoms = " ".join(disease["symptoms"]).lower()
    symptoms_text.append(symptoms)

# Train TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(symptoms_text)

# Save the trained model
model_data = {
    'vectorizer': vectorizer,
    'tfidf_matrix': tfidf_matrix,
    'diseases': diseases,
    'disease_data': {d["name"]: d for d in data["diseases"]}
}

with open("trained_model.pkl", "wb") as f:
    pickle.dump(model_data, f)

print(f"Model trained with {len(diseases)} diseases")
print("Saved to trained_model.pkl")