from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load datasets
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "health_dataset.json")
DIET_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "enhanced_diet_dataset.json")
MENTAL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "enhanced_mental_health_dataset.json")

DATASET = {}
DIET_DATA = {}
MENTAL_DATA = {}

try:
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        for disease in data.get("diseases", []):
            DATASET[disease["name"]] = {
                "symptoms": disease["symptoms"],
                "medicines": disease["medicines"],
                "prevention": disease.get("prevention", []),
                "home_care": disease.get("home_care", []),
                "advice": f"{disease['description']} {disease.get('note', '')}"
            }
    print(f"Loaded {len(DATASET)} diseases")
except:
    print("Health dataset not found")

try:
    with open(DIET_PATH, "r", encoding="utf-8") as f:
        diet_data = json.load(f)
        for plan in diet_data.get("diet_plans", []):
            DIET_DATA[plan["condition"]] = {
                "keywords": plan["keywords"],
                "diet_plan": plan["diet_plan"]
            }
    print(f"Loaded {len(DIET_DATA)} diet plans")
except:
    print("Diet dataset not found")

try:
    with open(MENTAL_PATH, "r", encoding="utf-8") as f:
        mental_data = json.load(f)
        for condition in mental_data.get("mental_health", []):
            MENTAL_DATA[condition["condition"]] = {
                "keywords": condition["keywords"],
                "support": condition["support"]
            }
    print(f"Loaded {len(MENTAL_DATA)} mental health conditions")
except:
    print("Mental health dataset not found")

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

@app.get("/")
def root():
    return {"message": "Healthy India API running", "status": "healthy"}

def find_diet_plan(query):
    query_lower = query.lower()
    
    for condition, data in DIET_DATA.items():
        for keyword in data["keywords"]:
            if keyword in query_lower:
                plan = data["diet_plan"]
                return {
                    "type": "diet",
                    "condition": condition.replace("_", " ").title(),
                    "foods_to_eat": plan["foods_to_eat"],
                    "foods_to_avoid": plan["foods_to_avoid"],
                    "meal_timing": plan["meal_timing"],
                    "tips": plan["tips"]
                }
    return None

def find_mental_health_support(query):
    query_lower = query.lower()
    
    for condition, data in MENTAL_DATA.items():
        for keyword in data["keywords"]:
            if keyword in query_lower:
                support = data["support"]
                return {
                    "type": "mental_health",
                    "condition": condition.replace("_", " ").title(),
                    "symptoms": support.get("symptoms", []),
                    "coping_strategies": support["coping_strategies"],
                    "immediate_help": support["immediate_help"],
                    "professional_help": support["professional_help"],
                    "crisis_hotline": support.get("crisis_hotline", "")
                }
    return None

def find_match(symptoms):
    if not symptoms:
        return None
    
    query = " ".join(symptoms).lower()
    
    # Check for diet queries
    diet_keywords = ["diet", "food", "nutrition", "eat", "meal"]
    if any(keyword in query for keyword in diet_keywords):
        diet_result = find_diet_plan(query)
        if diet_result:
            return diet_result
    
    # Check for mental health queries
    mental_keywords = ["stress", "anxiety", "depression", "lonely", "mental", "mood", "sleep"]
    if any(keyword in query for keyword in mental_keywords):
        mental_result = find_mental_health_support(query)
        if mental_result:
            return mental_result
    
    # Regular disease matching
    if not DATASET:
        return None
    
    symptoms_lower = [s.lower().strip() for s in symptoms]
    best_match = None
    max_score = 0
    
    for disease, details in DATASET.items():
        disease_symptoms = [s.lower() for s in details.get("symptoms", [])]
        score = 0
        
        for user_symptom in symptoms_lower:
            for disease_symptom in disease_symptoms:
                if user_symptom in disease_symptom or disease_symptom in user_symptom:
                    score += 1
                    break
        
        # Boost COVID-19 for specific symptoms
        if disease == "COVID-19":
            covid_keywords = ["loss of taste", "loss of smell", "shortness of breath", "covid"]
            for keyword in covid_keywords:
                if any(keyword in s for s in symptoms_lower):
                    score += 2
                    break
        
        if score > max_score:
            max_score = score
            best_match = {
                "type": "disease",
                "disease": disease,
                "symptoms": details.get("symptoms", []),
                "medicines": details.get("medicines", []),
                "prevention": details.get("prevention", []),
                "home_care": details.get("home_care", []),
                "advice": details.get("advice", "")
            }
    
    return best_match if max_score > 0 else None

@app.post("/consult")
def consult(request: SymptomRequest):
    if not request.symptoms:
        raise HTTPException(status_code=400, detail="No symptoms provided")
    
    result = find_match(request.symptoms)
    if result:
        return {"source": "dataset", "result": result}
    
    return {"source": "gemini", "result": {"response": "No match found. Please consult a healthcare professional."}}

class ContactRequest(BaseModel):
    name: str
    email: str
    subject: str
    message: str

@app.post("/contact")
def contact(request: ContactRequest):
    try:
        # Fallback: mailto link
        subject = f"Healthy India Contact: {request.subject}"
        body = f"Name: {request.name}\nEmail: {request.email}\n\nMessage:\n{request.message}"
        return {"status": "fallback", "data": request.dict()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "dataset_loaded": len(DATASET) > 0,
        "diet_loaded": len(DIET_DATA) > 0,
        "mental_health_loaded": len(MENTAL_DATA) > 0,
        "gemini_configured": GEMINI_API_KEY is not None
    }