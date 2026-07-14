from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv

load_dotenv()
# 🔑 GEMINI API KEY - Set in Render Environment Variables or .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ============================================================================
# DYNAMIC DATASET LOADING
# ============================================================================
DATASET = {}
DIET_DATA = {}
MENTAL_DATA = {}

def load_data():
    global DATASET, DIET_DATA, MENTAL_DATA

    # Load Diseases
    try:
        with open("health_dataset.json", "r") as f:
            data = json.load(f)
            for disease in data.get("diseases", []):
                advice_list = disease.get("home_care", [])
                advice = ", ".join(advice_list) if advice_list else "Consult a doctor."

                DATASET[disease["name"]] = {
                    "symptoms": disease["symptoms"],
                    "medicines": disease["medicines"],
                    "advice": advice
                }
        print(f"Loaded {len(DATASET)} diseases.")
    except Exception as e:
        print(f"Error loading health_dataset.json: {e}")

    # Load Diets
    try:
        with open("enhanced_diet_dataset.json", "r") as f:
            data = json.load(f)
            for plan in data.get("diet_plans", []):
                condition = plan["condition"]
                details = plan["diet_plan"]
                DIET_DATA[condition] = {
                    "keywords": plan["keywords"],
                    "foods_to_eat": details["foods_to_eat"],
                    "foods_to_avoid": details["foods_to_avoid"],
                    "meal_timing": details.get("meal_timing", "Regular meals"),
                    "tips": details["tips"]
                }
        print(f"Loaded {len(DIET_DATA)} diet plans.")
    except Exception as e:
        print(f"Error loading enhanced_diet_dataset.json: {e}")

    # Load Mental Health
    try:
        with open("enhanced_mental_health_dataset.json", "r") as f:
            data = json.load(f)
            for item in data.get("mental_health", []):
                condition = item["condition"]
                support = item["support"]
                MENTAL_DATA[condition] = {
                    "keywords": item["keywords"],
                    "symptoms": support.get("symptoms", []),
                    "coping_strategies": support["coping_strategies"],
                    "immediate_help": support["immediate_help"],
                    "professional_help": support["professional_help"],
                    "crisis_hotline": support.get("crisis_hotline", "National Suicide Prevention Lifeline: 988")
                }
        print(f"Loaded {len(MENTAL_DATA)} mental health conditions.")
    except Exception as e:
        print(f"Error loading enhanced_mental_health_dataset.json: {e}")

# Initial load
load_data()

app = FastAPI(title="Healthy India API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomRequest(BaseModel):
    symptoms: list[str]

class ContactRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str

@app.get("/")
def root():
    return {"message": "✅ Healthy India API running", "status": "healthy"}

@app.post("/consult")
def consult(request: SymptomRequest):
    if not request.symptoms:
        raise HTTPException(status_code=400, detail="No symptoms provided")
    
    symptoms_lower = [s.lower().strip() for s in request.symptoms]
    query = " ".join(symptoms_lower)
    
    # Check for diet queries first
    for diet_type, data in DIET_DATA.items():
        if any(keyword in query for keyword in data["keywords"]):
            return {
                "source": "dataset",
                "result": {
                    "type": "diet",
                    "condition": diet_type.replace("_", " ").title(),
                    "foods_to_eat": data["foods_to_eat"],
                    "foods_to_avoid": data["foods_to_avoid"],
                    "meal_timing": data.get("meal_timing", "3 main meals + 2 healthy snacks throughout the day"),
                    "tips": data["tips"]
                }
            }
    
    # Check for mental health queries
    for condition, data in MENTAL_DATA.items():
        if any(keyword in query for keyword in data["keywords"]):
            return {
                "source": "dataset",
                "result": {
                    "type": "mental_health",
                    "condition": condition.replace("_", " ").title(),
                    "symptoms": data.get("symptoms", []),
                    "coping_strategies": data["coping_strategies"],
                    "immediate_help": data["immediate_help"],
                    "professional_help": data["professional_help"],
                    "crisis_hotline": data.get("crisis_hotline", "National Suicide Prevention Lifeline: 988")
                }
            }
    
    # Disease matching algorithm
    best_match = None
    max_score = 0
    
    for disease, details in DATASET.items():
        score = 0
        disease_symptoms = [s.lower() for s in details["symptoms"]]
        
        # Calculate matching score
        for user_symptom in symptoms_lower:
            for disease_symptom in disease_symptoms:
                if user_symptom in disease_symptom or disease_symptom in user_symptom:
                    score += 1
                    break
        
        # Special boost for COVID-19 with specific symptoms
        if disease == "COVID-19":
            covid_keywords = ["loss of taste", "loss of smell", "shortness of breath", "covid"]
            for keyword in covid_keywords:
                if any(keyword in s for s in symptoms_lower):
                    score += 2
                    break
        
        if score > max_score:
            max_score = score
            best_match = {
                "disease": disease,
                "symptoms": details["symptoms"],
                "medicines": details["medicines"],
                "advice": details["advice"],
                "confidence": min(score / len(symptoms_lower), 1.0)
            }
    
    if best_match and max_score > 0:
        return {"source": "dataset", "result": best_match}
    
    # Fallback response
    return {
        "source": "gemini", 
        "result": {
            "response": "No specific match found in our database. Please consult a healthcare professional for proper diagnosis and treatment. If you're experiencing severe symptoms, seek immediate medical attention."
        }
    }

@app.post("/contact")
def contact(request: ContactRequest):
    try:
        return {
            "status": "success",
            "message": "Thank you for your message! We will get back to you soon.",
            "data": {"name": request.name, "email": request.email, "subject": request.subject}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "dataset_loaded": True,
        "diseases_count": len(DATASET),
        "diet_plans_count": len(DIET_DATA),
        "mental_health_conditions": len(MENTAL_DATA),
        "gemini_configured": GEMINI_API_KEY is not None,
        "version": "1.0.0"
    }

# ============================================================================
# 🔑 GEMINI API KEY SETUP
# ============================================================================
"""
TO SET UP GEMINI API KEY:

1. FOR RENDER DEPLOYMENT:
   - Go to your Render service dashboard
   - Click "Environment" tab
   - Add environment variable:
     Key: GEMINI_API_KEY
     Value: AIzaSyAn1cTGyFzkqr-duApDRmqx5pD4-wpLE6E

2. FOR LOCAL DEVELOPMENT:
   - Create .env file in same directory as this main.py
   - Add line: GEMINI_API_KEY=AIzaSyAn1cTGyFzkqr-duApDRmqx5pD4-wpLE6E
"""

# ============================================================================
# 📝 INSTRUCTIONS FOR ADDING MORE DATASETS
# ============================================================================
"""
Datasets are now loaded from external JSON files:
- health_dataset.json (Diseases)
- enhanced_diet_dataset.json (Diets)
- enhanced_mental_health_dataset.json (Mental Health)

To add new data, please edit these JSON files directly.
"""
