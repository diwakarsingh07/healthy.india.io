from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
# 🔑 GEMINI API KEY - Set in Render Environment Variables or .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # AIzaSyAn1cTGyFzkqr-duApDRmqx5pD4-wpLE6E

# ============================================================================
# COMPLETE EMBEDDED DATASET - ALL 111 DISEASES
# ============================================================================
DATASET = {
    "Common Cold": {"symptoms": ["runny nose", "sore throat", "cough", "congestion", "headache", "sneezing", "fever"], "medicines": ["Decongestants", "Cough suppressants", "Pain relievers"], "advice": "Rest, stay hydrated, and consult a doctor if symptoms persist."},
    "Influenza": {"symptoms": ["fever", "muscle aches", "chills", "headache", "dry cough", "fatigue", "nasal congestion"], "medicines": ["Antiviral drugs", "Pain relievers", "Decongestants"], "advice": "Rest, hydration, and seek medical care for severe symptoms."},
    "COVID-19": {"symptoms": ["fever", "cough", "shortness of breath", "fatigue", "muscle aches", "headache", "loss of taste", "loss of smell", "sore throat"], "medicines": ["Antiviral medications", "Pain relievers"], "advice": "Isolate, rest, hydrate, and seek medical attention if symptoms worsen."},
    "Strep Throat": {"symptoms": ["severe sore throat", "painful swallowing", "fever", "red tonsils", "white patches", "swollen lymph nodes"], "medicines": ["Antibiotics", "Pain relievers"], "advice": "See a doctor for proper diagnosis and antibiotic treatment."},
    "Pneumonia": {"symptoms": ["chest pain", "cough with phlegm", "fatigue", "fever", "chills", "shortness of breath", "confusion"], "medicines": ["Antibiotics", "Cough medicine", "Fever reducers"], "advice": "Seek immediate medical attention. This is a serious condition."},
    "Bronchitis": {"symptoms": ["persistent cough", "mucus production", "fatigue", "shortness of breath", "chest discomfort", "fever"], "medicines": ["Cough medicine", "Bronchodilators", "Anti-inflammatory drugs"], "advice": "Rest, humidify air, stay hydrated, avoid lung irritants."},
    "Sinusitis": {"symptoms": ["thick nasal discharge", "nasal obstruction", "facial pain", "reduced smell", "cough", "fatigue"], "medicines": ["Nasal corticosteroids", "Decongestants", "Antibiotics"], "advice": "Use saline nasal spray, warm compresses, stay hydrated."},
    "Tuberculosis": {"symptoms": ["persistent cough", "coughing blood", "chest pain", "weight loss", "fatigue", "fever", "night sweats"], "medicines": ["Long-term antibiotics"], "advice": "Seek immediate medical attention. Complete full treatment course."},
    "Mononucleosis": {"symptoms": ["extreme fatigue", "sore throat", "fever", "swollen lymph nodes", "headache", "skin rash"], "medicines": ["Pain relievers", "Corticosteroids"], "advice": "Rest, hydration, avoid contact sports."},
    "UTI": {"symptoms": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain", "strong urge"], "medicines": ["Antibiotics", "Pain medication"], "advice": "Drink plenty of water, complete antibiotic course."},
    "Yeast Infection": {"symptoms": ["vaginal itching", "burning", "white discharge", "redness", "pain during intercourse"], "medicines": ["Antifungal creams", "Oral antifungals"], "advice": "Wear cotton underwear, avoid douches."},
    "Bacterial Vaginosis": {"symptoms": ["gray discharge", "fishy odor", "vaginal itching", "burning urination"], "medicines": ["Antibiotics"], "advice": "Complete antibiotic course, practice good hygiene."},
    "Hepatitis A": {"symptoms": ["fatigue", "nausea", "abdominal pain", "jaundice", "fever", "loss of appetite"], "medicines": ["Supportive care", "Vaccination"], "advice": "Rest, hydration, avoid alcohol."},
    "Hepatitis B": {"symptoms": ["abdominal pain", "dark urine", "fever", "joint pain", "jaundice", "nausea"], "medicines": ["Antiviral drugs", "Interferon"], "advice": "Follow medical advice, avoid alcohol."},
    "Hepatitis C": {"symptoms": ["fatigue", "poor appetite", "jaundice", "dark urine", "itchy skin"], "medicines": ["Antiviral medications"], "advice": "Take prescribed medications, regular doctor visits."},
    "HIV/AIDS": {"symptoms": ["fever", "fatigue", "swollen lymph nodes", "weight loss", "infections"], "medicines": ["Antiretroviral therapy"], "advice": "Take medications exactly as prescribed, healthy lifestyle."},
    "Chlamydia": {"symptoms": ["painful urination", "discharge", "pain during sex", "abdominal pain"], "medicines": ["Antibiotics"], "advice": "Complete medication, notify partners, abstain during treatment."},
    "Gonorrhea": {"symptoms": ["thick discharge", "painful urination", "anal itching", "sore throat"], "medicines": ["Antibiotics"], "advice": "Complete medication, partner notification, follow-up testing."},
    "Herpes": {"symptoms": ["painful blisters", "itching", "burning sensation", "flu-like symptoms"], "medicines": ["Antiviral drugs"], "advice": "Keep sores clean, wear loose clothing, avoid sex during outbreaks."},
    "HPV": {"symptoms": ["genital warts", "common warts", "often asymptomatic"], "medicines": ["Wart treatments"], "advice": "Regular health screenings, HPV vaccination."},
    "Syphilis": {"symptoms": ["chancre sores", "skin rash", "fever", "fatigue", "headache"], "medicines": ["Antibiotics"], "advice": "Complete antibiotics, partner notification, follow-up tests."},
    "Conjunctivitis": {"symptoms": ["redness", "itchiness", "discharge", "tearing", "crusting"], "medicines": ["Antibiotic drops", "Antihistamines"], "advice": "Don't touch eyes, wash hands frequently."},
    "Gastroenteritis": {"symptoms": ["diarrhea", "abdominal cramps", "nausea", "vomiting", "fever"], "medicines": ["Supportive care", "Anti-diarrheals"], "advice": "Stay hydrated, BRAT diet, rest."},
    "Food Poisoning": {"symptoms": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever"], "medicines": ["Fluid replacement", "Antibiotics if needed"], "advice": "Stay hydrated, rest, gradual return to eating."},
    "Norovirus": {"symptoms": ["nausea", "vomiting", "stomach pain", "diarrhea", "fever"], "medicines": ["Supportive care"], "advice": "Drink fluids, rest, eat bland foods."},
    "Appendicitis": {"symptoms": ["abdominal pain", "nausea", "vomiting", "fever", "loss of appetite"], "medicines": ["Surgery", "Antibiotics"], "advice": "Medical emergency - seek immediate care."},
    "Cellulitis": {"symptoms": ["red swollen skin", "pain", "tenderness", "fever"], "medicines": ["Antibiotics"], "advice": "Rest, elevate affected area, take all antibiotics."},
    "Athletes Foot": {"symptoms": ["itchy rash", "burning", "blisters", "cracking skin"], "medicines": ["Antifungal creams", "Oral antifungals"], "advice": "Keep feet dry, wear breathable shoes."},
    "Ringworm": {"symptoms": ["ring-shaped rash", "itchy skin", "scaly patches"], "medicines": ["Antifungal creams", "Oral antifungals"], "advice": "Keep area dry, don't share clothing."},
    "Impetigo": {"symptoms": ["red sores", "honey-colored crusts", "itching"], "medicines": ["Topical antibiotics", "Oral antibiotics"], "advice": "Keep sores clean, avoid contact with others."},
    "Shingles": {"symptoms": ["pain", "burning", "red rash", "blisters", "itching", "fever"], "medicines": ["Antiviral drugs", "Pain relievers"], "advice": "Cool compresses, avoid scratching, rest."},
    "Chickenpox": {"symptoms": ["itchy rash", "blisters", "fever", "fatigue", "headache"], "medicines": ["Supportive care", "Antivirals for high-risk"], "advice": "Don't scratch, oatmeal baths, trim nails."},
    "Measles": {"symptoms": ["high fever", "cough", "runny nose", "red eyes", "red rash"], "medicines": ["Supportive care", "Vitamin A"], "advice": "Rest, hydration, isolation."},
    "Mumps": {"symptoms": ["swollen glands", "fever", "headache", "muscle aches", "fatigue"], "medicines": ["Supportive care"], "advice": "Rest, soft foods, warm compresses."},
    "Rubella": {"symptoms": ["mild fever", "headache", "runny nose", "red eyes", "pink rash"], "medicines": ["Supportive care"], "advice": "Rest, fever reducers, isolate from pregnant women."},
    "Malaria": {"symptoms": ["high fever", "chills", "headache", "nausea", "muscle pain"], "medicines": ["Antimalarial drugs"], "advice": "Seek immediate medical attention."},
    "Dengue": {"symptoms": ["high fever", "severe headache", "eye pain", "joint pain", "rash"], "medicines": ["Supportive care", "Pain relievers"], "advice": "Rest, hydration, avoid aspirin."},
    "Lyme Disease": {"symptoms": ["bulls-eye rash", "fever", "chills", "fatigue", "body aches"], "medicines": ["Antibiotics"], "advice": "Complete antibiotic course, remove ticks promptly."},
    "Tetanus": {"symptoms": ["jaw cramping", "muscle stiffness", "trouble swallowing", "spasms"], "medicines": ["Emergency medical care"], "advice": "Medical emergency - seek immediate care."},
    "Whooping Cough": {"symptoms": ["runny nose", "mild cough", "rapid coughs", "vomiting"], "medicines": ["Antibiotics"], "advice": "Rest, small meals, avoid irritants."},
    "Meningitis": {"symptoms": ["high fever", "stiff neck", "severe headache", "nausea", "confusion"], "medicines": ["Emergency antibiotics"], "advice": "Medical emergency - seek immediate care."},
    "Hypertension": {"symptoms": ["often no symptoms", "headaches", "shortness of breath"], "medicines": ["Blood pressure medications"], "advice": "Low salt diet, exercise, monitor blood pressure."},
    "Heart Disease": {"symptoms": ["chest pain", "shortness of breath", "fatigue"], "medicines": ["Heart medications"], "advice": "Healthy lifestyle, take medications, cardiac rehab."},
    "Heart Failure": {"symptoms": ["shortness of breath", "fatigue", "swelling", "rapid heartbeat"], "medicines": ["Heart medications", "Diuretics"], "advice": "Monitor weight daily, low-sodium diet, take medications."},
    "Heart Attack": {"symptoms": ["chest pain", "arm pain", "shortness of breath", "cold sweat"], "medicines": ["Emergency care"], "advice": "Call emergency services immediately."},
    "Stroke": {"symptoms": ["face drooping", "arm weakness", "speech difficulty", "confusion"], "medicines": ["Emergency care"], "advice": "Act FAST - call emergency services."},
    "High Cholesterol": {"symptoms": ["no symptoms"], "medicines": ["Statins", "Cholesterol medications"], "advice": "Healthy diet, exercise, take medications."},
    "Type 1 Diabetes": {"symptoms": ["increased thirst", "frequent urination", "hunger", "weight loss"], "medicines": ["Insulin"], "advice": "Monitor blood sugar, insulin administration, carb counting."},
    "Type 2 Diabetes": {"symptoms": ["increased thirst", "frequent urination", "hunger", "fatigue", "blurred vision"], "medicines": ["Diabetes medications", "Insulin"], "advice": "Monitor blood sugar, healthy diet, exercise."},
    "Hypothyroidism": {"symptoms": ["fatigue", "weight gain", "cold intolerance", "dry skin"], "medicines": ["Thyroid hormone replacement"], "advice": "Take medication consistently, regular monitoring."},
    "Hyperthyroidism": {"symptoms": ["weight loss", "rapid heartbeat", "nervousness", "tremors"], "medicines": ["Anti-thyroid medications"], "advice": "Take medications, follow up with specialist."},
    "Asthma": {"symptoms": ["shortness of breath", "chest tightness", "wheezing", "coughing"], "medicines": ["Inhalers", "Bronchodilators"], "advice": "Avoid triggers, use action plan, take controller medications."},
    "COPD": {"symptoms": ["shortness of breath", "wheezing", "chest tightness", "chronic cough"], "medicines": ["Bronchodilators", "Inhaled steroids"], "advice": "Don't smoke, pulmonary rehabilitation."},
    "Kidney Disease": {"symptoms": ["nausea", "vomiting", "fatigue", "swelling", "urination changes"], "medicines": ["Blood pressure medications", "Diuretics"], "advice": "Low-sodium diet, take medications, regular checkups."},
    "Kidney Stones": {"symptoms": ["severe pain", "painful urination", "pink urine", "nausea"], "medicines": ["Pain relievers", "Alpha blockers"], "advice": "Drink plenty of water, strain urine."},
    "Gout": {"symptoms": ["intense joint pain", "inflammation", "redness", "limited motion"], "medicines": ["NSAIDs", "Colchicine", "Allopurinol"], "advice": "Rest joint, ice, elevate, stay hydrated."},
    "Osteoarthritis": {"symptoms": ["joint pain", "stiffness", "tenderness", "loss of flexibility"], "medicines": ["NSAIDs", "Pain relievers"], "advice": "Exercise, weight management, heat/cold therapy."},
    "Rheumatoid Arthritis": {"symptoms": ["tender swollen joints", "morning stiffness", "fatigue"], "medicines": ["DMARDs", "Biologics"], "advice": "Regular exercise, stress management."},
    "Osteoporosis": {"symptoms": ["back pain", "loss of height", "stooped posture"], "medicines": ["Bisphosphonates", "Calcium", "Vitamin D"], "advice": "Weight-bearing exercise, fall prevention."},
    "Fibromyalgia": {"symptoms": ["widespread pain", "fatigue", "cognitive difficulties", "sleep problems"], "medicines": ["Pain relievers", "Antidepressants"], "advice": "Stress reduction, gentle exercise, good sleep."},
    "Chronic Fatigue": {"symptoms": ["severe fatigue", "post-exertional malaise", "sleep problems"], "medicines": ["Symptom-focused medications"], "advice": "Pacing activity, sleep management."},
    "Epilepsy": {"symptoms": ["seizures", "confusion", "staring spells", "jerking movements"], "medicines": ["Anti-seizure medications"], "advice": "Take medication consistently, wear medical alert."},
    "Alzheimers": {"symptoms": ["memory loss", "confusion", "difficulty planning", "personality changes"], "medicines": ["Cholinesterase inhibitors"], "advice": "Routine, safe environment, caregiver support."},
    "Parkinsons": {"symptoms": ["tremor", "slowed movement", "rigid muscles", "balance problems"], "medicines": ["Levodopa", "Dopamine agonists"], "advice": "Physical therapy, exercise, fall prevention."},
    "Multiple Sclerosis": {"symptoms": ["numbness", "weakness", "vision problems", "fatigue"], "medicines": ["Disease-modifying therapies"], "advice": "Physical therapy, manage heat sensitivity."},
    "Migraines": {"symptoms": ["throbbing pain", "light sensitivity", "nausea", "vomiting"], "medicines": ["Triptans", "Pain relievers", "Preventive medications"], "advice": "Rest in dark room, identify triggers."},
    "Tension Headaches": {"symptoms": ["dull aching pain", "tightness", "tenderness"], "medicines": ["Pain relievers", "Preventive medications"], "advice": "Stress management, regular exercise."},
    "Anxiety": {"symptoms": ["nervousness", "increased heart rate", "sweating", "trembling"], "medicines": ["Antidepressants", "Anti-anxiety medications"], "advice": "Stress management, therapy, regular exercise."},
    "Depression": {"symptoms": ["sadness", "loss of interest", "fatigue", "sleep changes"], "medicines": ["Antidepressants"], "advice": "Seek professional help, maintain treatment plan."},
    "Bipolar Disorder": {"symptoms": ["mood swings", "mania", "depression", "energy changes"], "medicines": ["Mood stabilizers", "Antipsychotics"], "advice": "Strict medication adherence, regular therapy."},
    "Schizophrenia": {"symptoms": ["delusions", "hallucinations", "disorganized thinking"], "medicines": ["Antipsychotics"], "advice": "Medication adherence, therapy, family support."},
    "ADHD": {"symptoms": ["inattention", "hyperactivity", "impulsivity", "disorganization"], "medicines": ["Stimulants", "Non-stimulants"], "advice": "Behavioral therapy, organization strategies."},
    "Autism": {"symptoms": ["social challenges", "communication difficulties", "repetitive behaviors"], "medicines": ["Symptom-specific medications"], "advice": "Behavioral therapy, structured schedules."},
    "IBS": {"symptoms": ["abdominal pain", "bloating", "gas", "diarrhea", "constipation"], "medicines": ["Fiber supplements", "Antispasmodics"], "advice": "FODMAP diet, stress reduction."},
    "Crohns Disease": {"symptoms": ["diarrhea", "abdominal pain", "blood in stool", "weight loss"], "medicines": ["Anti-inflammatory drugs", "Biologics"], "advice": "Diet modifications, stress management."},
    "Ulcerative Colitis": {"symptoms": ["bloody diarrhea", "abdominal pain", "urgency", "fatigue"], "medicines": ["Anti-inflammatories", "Immunosuppressants"], "advice": "Diet changes, stress reduction."},
    "Celiac Disease": {"symptoms": ["diarrhea", "fatigue", "weight loss", "bloating"], "medicines": ["Gluten-free diet"], "advice": "Strict gluten-free diet, nutritional counseling."},
    "GERD": {"symptoms": ["heartburn", "regurgitation", "chest pain", "difficulty swallowing"], "medicines": ["Proton pump inhibitors", "H2 blockers"], "advice": "Elevate head of bed, avoid trigger foods."},
    "Peptic Ulcers": {"symptoms": ["burning stomach pain", "bloating", "heartburn", "nausea"], "medicines": ["Antibiotics", "Acid reducers"], "advice": "Avoid NSAIDs, don't smoke."},
    "Cirrhosis": {"symptoms": ["fatigue", "easy bruising", "jaundice", "swelling"], "medicines": ["Medications for complications"], "advice": "Stop drinking alcohol, low-sodium diet."},
    "Fatty Liver": {"symptoms": ["often none", "fatigue", "abdominal pain"], "medicines": ["Control underlying causes"], "advice": "Weight loss, control diabetes, avoid alcohol."},
    "Anemia": {"symptoms": ["fatigue", "weakness", "pale skin", "shortness of breath"], "medicines": ["Iron supplements", "B12 supplements"], "advice": "Iron-rich diet, treat underlying causes."},
    "Hemophilia": {"symptoms": ["excessive bleeding", "deep bruises", "joint pain"], "medicines": ["Clotting factor replacement"], "advice": "Avoid injury, regular exercise."},
    "Blood Clots": {"symptoms": ["leg swelling", "pain", "redness", "warmth"], "medicines": ["Blood thinners"], "advice": "Take medications, wear compression stockings."},
    "Psoriasis": {"symptoms": ["red scaly patches", "itching", "burning"], "medicines": ["Topical treatments", "Biologics"], "advice": "Moisturize, avoid triggers."},
    "Eczema": {"symptoms": ["itchy skin", "red patches", "dry skin"], "medicines": ["Topical steroids", "Moisturizers"], "advice": "Avoid scratching, moisturize frequently."},
    "Acne": {"symptoms": ["whiteheads", "blackheads", "pimples", "cysts"], "medicines": ["Topical treatments", "Oral medications"], "advice": "Don't pick, gentle cleansing."},
    "Rosacea": {"symptoms": ["facial redness", "visible blood vessels", "bumps"], "medicines": ["Topical treatments", "Oral antibiotics"], "advice": "Avoid triggers, sun protection."},
    "Hives": {"symptoms": ["raised welts", "intense itching"], "medicines": ["Antihistamines", "Corticosteroids"], "advice": "Avoid triggers, cool compresses."},
    "Lupus": {"symptoms": ["butterfly rash", "fatigue", "joint pain", "fever"], "medicines": ["Immunosuppressants", "Anti-malarials"], "advice": "Sun protection, regular exercise."},
    "Sleep Apnea": {"symptoms": ["loud snoring", "gasping", "morning headache", "daytime sleepiness"], "medicines": ["CPAP machine"], "advice": "Lose weight, sleep on side."},
    "Insomnia": {"symptoms": ["difficulty falling asleep", "waking during night", "daytime tiredness"], "medicines": ["Sleep aids", "Melatonin"], "advice": "Sleep hygiene, relaxation techniques."},
    "Obesity": {"symptoms": ["excessive body fat", "difficulty with activities"], "medicines": ["Weight-loss medications"], "advice": "Calorie-controlled diet, increased activity."},
    "Lung Cancer": {"symptoms": ["new cough", "coughing blood", "shortness of breath", "chest pain"], "medicines": ["Specialized cancer treatment"], "advice": "Don't smoke, seek specialized care."},
    "Breast Cancer": {"symptoms": ["lump in breast", "breast changes", "nipple discharge"], "medicines": ["Specialized cancer treatment"], "advice": "Regular screening, seek specialized care."},
    "Prostate Cancer": {"symptoms": ["trouble urinating", "blood in semen", "pelvic discomfort"], "medicines": ["Specialized cancer treatment"], "advice": "Regular screening, seek specialized care."},
    "Colorectal Cancer": {"symptoms": ["bowel changes", "blood in stool", "abdominal discomfort"], "medicines": ["Specialized cancer treatment"], "advice": "Regular screening, healthy diet."},
    "Skin Cancer": {"symptoms": ["changing mole", "new growth", "sore that doesn't heal"], "medicines": ["Surgical treatment"], "advice": "Sun protection, regular skin exams."},
    "Enlarged Prostate": {"symptoms": ["frequent urination", "weak stream", "urgency"], "medicines": ["Alpha blockers", "5-alpha reductase inhibitors"], "advice": "Limit evening fluids, double void."},
    "Erectile Dysfunction": {"symptoms": ["trouble getting erection", "trouble keeping erection"], "medicines": ["PDE5 inhibitors"], "advice": "Exercise, healthy weight, manage stress."},
    "PCOS": {"symptoms": ["irregular periods", "excess hair", "weight gain"], "medicines": ["Birth control pills", "Metformin"], "advice": "Healthy weight, exercise, low-carb diet."},
    "Endometriosis": {"symptoms": ["painful periods", "pain with intercourse", "heavy bleeding"], "medicines": ["Pain relievers", "Hormone therapy"], "advice": "Heat therapy, regular exercise."},
    "Uterine Fibroids": {"symptoms": ["heavy bleeding", "pelvic pain", "frequent urination"], "medicines": ["NSAIDs", "Hormone therapy"], "advice": "Heat for cramps, healthy weight."},
    "Menopause": {"symptoms": ["hot flashes", "night sweats", "mood changes", "irregular periods"], "medicines": ["Hormone therapy", "Antidepressants"], "advice": "Cooling techniques, regular exercise."},
    "Cataracts": {"symptoms": ["clouded vision", "difficulty at night", "light sensitivity"], "medicines": ["Surgery"], "advice": "Brighter lights, anti-glare sunglasses."},
    "Glaucoma": {"symptoms": ["initially none", "blind spots", "tunnel vision"], "medicines": ["Eye drops", "Surgery"], "advice": "Use drops as prescribed, regular eye exams."},
    "Macular Degeneration": {"symptoms": ["central vision loss", "distorted vision"], "medicines": ["Anti-VEGF injections"], "advice": "AREDS supplements, eat leafy greens."},
    "Tinnitus": {"symptoms": ["ringing", "buzzing", "roaring in ears"], "medicines": ["Treat underlying cause"], "advice": "White noise machines, stress reduction."},
    "Hearing Loss": {"symptoms": ["muffled speech", "difficulty understanding", "turning up volume"], "medicines": ["Hearing aids", "Treat underlying cause"], "advice": "Face people when they speak, protect ears."},
    "Carpal Tunnel": {"symptoms": ["numbness in fingers", "weakness", "tingling"], "medicines": ["NSAIDs", "Steroid injections"], "advice": "Wrist splinting, take breaks, stretching."},
    "Plantar Fasciitis": {"symptoms": ["heel pain", "morning pain", "pain after standing"], "medicines": ["NSAIDs", "Steroid injections"], "advice": "Rest, ice, stretching, supportive shoes."}
}

# ============================================================================
# ALL DIET PLANS - COMPLETE ENHANCED DATASET
# ============================================================================
DIET_DATA = {
    "diabetes": {"keywords": ["diabetes", "blood sugar", "diabetic", "insulin", "glucose"], "foods_to_eat": ["Leafy greens", "Whole grains", "Lean proteins", "Nuts", "Berries", "Fish", "Avocado", "Beans"], "foods_to_avoid": ["White bread", "Sugary drinks", "Processed foods", "Fried foods", "Sweets", "White rice"], "tips": ["Monitor blood sugar regularly", "Stay hydrated", "Exercise after meals", "Count carbohydrates"]},
    "weight_loss": {"keywords": ["weight loss", "lose weight", "obesity", "fat loss", "slim down", "diet plan"], "foods_to_eat": ["Vegetables", "Fruits", "Lean meats", "Eggs", "Greek yogurt", "Quinoa", "Oats", "Legumes"], "foods_to_avoid": ["Fast food", "Sugary snacks", "Alcohol", "Refined carbs", "Processed meats", "Soda"], "tips": ["Drink water before meals", "Eat slowly", "Control portions", "Exercise regularly", "Track calories"]},
    "heart_health": {"keywords": ["heart", "cardiac", "cholesterol", "blood pressure", "hypertension", "cardiovascular"], "foods_to_eat": ["Salmon", "Oats", "Berries", "Dark chocolate", "Tomatoes", "Almonds", "Olive oil", "Spinach"], "foods_to_avoid": ["Trans fats", "Excess salt", "Red meat", "Sugary foods", "Processed foods", "Butter"], "tips": ["Limit sodium intake", "Choose healthy fats", "Eat more fiber", "Follow DASH diet principles"]},
    "mediterranean": {"keywords": ["mediterranean", "longevity", "brain health", "olive oil"], "foods_to_eat": ["Fruits", "Vegetables", "Whole grains", "Legumes", "Nuts", "Olive oil", "Fish", "Poultry"], "foods_to_avoid": ["Processed foods", "Red meat", "Refined sugars", "Trans fats"], "tips": ["Use olive oil as primary fat", "Eat fish twice weekly", "Enjoy meals socially", "Moderate wine consumption"]},
    "keto": {"keywords": ["keto", "ketogenic", "low carb", "high fat", "ketosis"], "foods_to_eat": ["Meat", "Fish", "Eggs", "Cheese", "Nuts", "Avocado", "Leafy greens", "Coconut oil"], "foods_to_avoid": ["Grains", "Sugar", "Fruits", "Potatoes", "Bread", "Pasta", "Rice"], "tips": ["Stay hydrated", "Monitor ketones", "Increase electrolytes", "Gradual transition"]},
    "plant_based": {"keywords": ["vegan", "vegetarian", "plant based", "no meat", "dairy free"], "foods_to_eat": ["Fruits", "Vegetables", "Legumes", "Nuts", "Seeds", "Whole grains", "Tofu", "Tempeh"], "foods_to_avoid": ["Meat", "Dairy", "Eggs", "Honey", "Gelatin", "Animal products"], "tips": ["Supplement B12", "Combine proteins", "Eat variety of colors", "Include iron-rich foods"]}
}

# ============================================================================
# ALL MENTAL HEALTH CONDITIONS - COMPLETE ENHANCED DATASET
# ============================================================================
MENTAL_DATA = {
    "stress": {"keywords": ["stress", "stressed", "anxiety", "tension", "overwhelmed", "pressure", "stress management"], "symptoms": ["Headaches", "Muscle tension", "Sleep problems", "Irritability", "Fatigue", "Racing thoughts"], "coping_strategies": ["Diaphragmatic breathing", "Progressive muscle relaxation", "Mindfulness meditation", "Regular exercise", "Social connection", "Time management"], "immediate_help": ["Take 10 deep breaths", "Go for a walk", "Listen to calming music", "Practice mindfulness", "Call a friend"], "professional_help": "Consider counseling if stress persists for more than 2 weeks or interferes with daily life", "techniques": ["4-7-8 breathing technique", "Body scan meditation", "Cognitive restructuring", "Gratitude practice"]},
    "loneliness": {"keywords": ["lonely", "loneliness", "isolated", "alone", "social isolation", "disconnected"], "symptoms": ["Sadness", "Empty feelings", "Lack of energy", "Sleep issues", "Loss of appetite", "Social withdrawal"], "coping_strategies": ["Join social groups", "Volunteer", "Call friends/family", "Take up hobbies", "Pet therapy", "Online communities"], "immediate_help": ["Call a friend", "Go to public places", "Join online communities", "Practice self-care", "Write in journal"], "professional_help": "Seek therapy if loneliness affects daily functioning or leads to depression", "techniques": ["Gradual social exposure", "Building social skills", "Self-compassion practice"]},
    "sleep_problems": {"keywords": ["insomnia", "sleep", "sleepless", "tired", "fatigue", "sleep disorder", "can't sleep"], "symptoms": ["Difficulty falling asleep", "Frequent waking", "Daytime fatigue", "Irritability", "Concentration problems"], "coping_strategies": ["Consistent sleep schedule", "Dark, cool room", "Limit screen time", "Avoid caffeine", "Relaxation routine", "Morning sunlight"], "immediate_help": ["Try deep breathing", "Read a book", "Warm bath", "Herbal tea", "Progressive muscle relaxation"], "professional_help": "See doctor if sleep problems persist for more than 3 weeks", "techniques": ["Sleep hygiene", "Stimulus control", "Sleep restriction", "Cognitive behavioral therapy for insomnia"]},
    "depression": {"keywords": ["depression", "depressed", "sad", "hopeless", "worthless", "suicidal", "down", "blue"], "symptoms": ["Persistent sadness", "Loss of interest", "Fatigue", "Sleep changes", "Appetite changes", "Guilt", "Concentration problems"], "coping_strategies": ["Regular exercise", "Social support", "Healthy routine", "Mindfulness", "Journaling", "Behavioral activation"], "immediate_help": ["Reach out to someone", "Practice self-care", "Avoid alcohol", "Get sunlight", "Engage in pleasant activities"], "professional_help": "Seek immediate help if having suicidal thoughts. Call emergency services or crisis hotline.", "crisis_hotline": "National Suicide Prevention Lifeline: 988", "techniques": ["Cognitive behavioral therapy", "Mindfulness-based therapy", "Interpersonal therapy"]},
    "anxiety": {"keywords": ["anxiety", "anxious", "panic", "worry", "fear", "nervous", "panic attack"], "symptoms": ["Excessive worry", "Restlessness", "Fatigue", "Difficulty concentrating", "Muscle tension", "Sleep disturbance"], "coping_strategies": ["Deep breathing", "Grounding techniques", "Regular exercise", "Limit caffeine", "Challenge negative thoughts", "Relaxation techniques"], "immediate_help": ["5-4-3-2-1 grounding technique", "Deep breathing", "Progressive muscle relaxation", "Call support person"], "professional_help": "Consider therapy if anxiety interferes with daily activities or relationships", "techniques": ["Exposure therapy", "Cognitive restructuring", "Mindfulness-based stress reduction", "Acceptance and commitment therapy"]},
    "reproductive_health": {"keywords": ["reproductive health", "menstrual", "pregnancy", "fertility", "sexual health", "pms", "periods"], "symptoms": ["Irregular periods", "Pelvic pain", "Mood changes", "Fertility concerns", "Sexual dysfunction"], "coping_strategies": ["Track menstrual cycle", "Healthy diet", "Regular exercise", "Stress management", "Safe sex practices", "Regular screenings"], "immediate_help": ["Use heating pad for cramps", "Stay hydrated", "Rest when needed", "Practice relaxation"], "professional_help": "Consult gynecologist for persistent issues, irregular cycles, or fertility concerns", "techniques": ["Mindful eating", "Stress reduction", "Body awareness", "Communication skills"]},
    "happiness": {"keywords": ["happiness", "joy", "well-being", "positive", "life satisfaction", "fulfillment"], "symptoms": ["Low mood", "Lack of motivation", "Feeling unfulfilled", "Loss of pleasure"], "coping_strategies": ["Cultivate gratitude", "Build social connections", "Acts of kindness", "Find purpose", "Practice mindfulness", "Exercise regularly"], "immediate_help": ["Practice gratitude", "Connect with loved ones", "Engage in enjoyable activities", "Spend time in nature"], "professional_help": "Consider positive psychology coaching or therapy to enhance well-being", "techniques": ["Gratitude journaling", "Savoring experiences", "Character strengths identification", "Flow activities"]}
}

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
                    "meal_timing": "3 main meals + 2 healthy snacks throughout the day",
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
🏥 TO ADD MORE DISEASES:
1. Find the DATASET dictionary above (around line 10)
2. Add new entry:
   "Disease Name": {
       "symptoms": ["symptom1", "symptom2"],
       "medicines": ["medicine1", "medicine2"],
       "advice": "Medical advice"
   },

🥗 TO ADD MORE DIET PLANS:
1. Find the DIET_DATA dictionary above (around line 120)
2. Add new entry:
   "diet_name": {
       "keywords": ["keyword1", "keyword2"],
       "foods_to_eat": ["food1", "food2"],
       "foods_to_avoid": ["food1", "food2"],
       "tips": ["tip1", "tip2"]
   },

🧠 TO ADD MORE MENTAL HEALTH CONDITIONS:
1. Find the MENTAL_DATA dictionary above (around line 130)
2. Add new entry:
   "condition_name": {
       "keywords": ["keyword1", "keyword2"],
       "symptoms": ["symptom1", "symptom2"],
       "coping_strategies": ["strategy1", "strategy2"],
       "immediate_help": ["help1", "help2"],
       "professional_help": "Professional advice text"
   },

🚀 DEPLOYMENT:
1. Save as main.py
2. Upload to GitHub
3. Deploy on Render with environment variable GEMINI_API_KEY
"""
