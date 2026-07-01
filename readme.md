# Healthy India - AI-Powered Healthcare Assistant

A comprehensive healthcare assistant application with FastAPI backend and React Native frontend.

## 🏗️ Project Structure

```
healthy-india/
├── backend/
│   ├── app_backend/          # Main FastAPI application
│   │   ├── app/
│   │   │   ├── main.py       # FastAPI app with health consultation endpoints
│   │   │   └── dataset.json  # Medical conditions database
│   │   ├── .env              # Environment variables
│   │   ├── requirements.txt  # Python dependencies
│   │   └── run.py           # Server startup script
│   ├── dataset_helper.py     # Legacy helper (deprecated)
│   ├── gemini_helper.py      # Legacy helper (deprecated)
│   └── health_dataset.json   # Comprehensive medical database
├── frontend/
│   └── mobile/
│       ├── api.js           # API client for React Native
│       ├── App.js           # Main React Native app
│       └── package.json     # Node.js dependencies
└── README.md
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend/app_backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Edit `.env` file
   - Add your Gemini API key: `GEMINI_API_KEY=your_actual_api_key_here`

4. **Start the server:**
   ```bash
   python run.py
   ```

   The API will be available at:
   - **API Base:** http://localhost:8000
   - **Documentation:** http://localhost:8000/docs
   - **Health Check:** http://localhost:8000/health

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend/mobile
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the React Native app:**
   ```bash
   npm start
   ```

## 📡 API Endpoints

### `GET /`
Health check endpoint
```json
{
  "message": "✅ Healthy India API running",
  "status": "healthy"
}
```

### `POST /consult`
Main consultation endpoint
```json
{
  "symptoms": ["fever", "cough", "headache"]
}
```

**Response (Dataset Match):**
```json
{
  "source": "dataset",
  "result": {
    "disease": "Common Cold",
    "symptoms": ["runny nose", "sore throat", "cough"],
    "medicines": ["Decongestants", "Pain relievers"],
    "advice": "Rest, stay hydrated, and consult a doctor if symptoms persist."
  }
}
```

**Response (AI Fallback):**
```json
{
  "source": "gemini",
  "result": {
    "response": "Based on your symptoms, you might have..."
  }
}
```

### `GET /health`
System health status
```json
{
  "status": "healthy",
  "dataset_loaded": true,
  "gemini_configured": true
}
```

## 🔧 Configuration

### Environment Variables (.env)
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Getting Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 🏥 Medical Database

The application uses a two-tier approach:

1. **Primary Dataset** (`dataset.json`): Quick symptom matching for common conditions
2. **AI Fallback** (Gemini): Advanced analysis for complex or unmatched symptoms

### Adding New Conditions

Edit `app/dataset.json`:
```json
{
  "Condition Name": {
    "symptoms": ["symptom1", "symptom2"],
    "medicines": ["medicine1", "medicine2"],
    "advice": "Medical advice and recommendations"
  }
}
```

## 🧪 Testing

### Test the API directly:
```bash
curl -X POST "http://localhost:8000/consult" \
     -H "Content-Type: application/json" \
     -d '{"symptoms": ["fever", "cough"]}'
```

### Health Check:
```bash
curl http://localhost:8000/health
```

## 📱 Mobile App Integration

The React Native app uses the API client in `frontend/mobile/api.js`:

```javascript
import { consult, healthCheck } from './api.js';

// Check symptoms
const result = await consult(['fever', 'headache']);

// Check server health
const health = await healthCheck();
```

## 🛠️ Development

### Running in Development Mode
```bash
# Backend (with auto-reload)
cd backend/app_backend
python run.py

# Frontend (with hot reload)
cd frontend/mobile
npm start
```

### Adding New Features
1. **Backend**: Modify `app/main.py`
2. **Frontend**: Update `App.js` and `api.js`
3. **Database**: Edit `dataset.json`

## 🚨 Important Notes

- **Medical Disclaimer**: This application is for educational purposes only
- **Always consult healthcare professionals** for medical advice
- **API Key Security**: Never commit real API keys to version control
- **CORS**: Currently configured for development (allow all origins)

## 📋 Dependencies

### Backend (Python)
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variables
- `google-generativeai` - Gemini AI integration

### Frontend (React Native)
- `axios` - HTTP client
- `react-native` - Mobile framework

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Check `.env` file configuration
3. **CORS Errors**: Verify frontend is using correct backend URL
4. **Port Conflicts**: Change port in `run.py` if 8000 is occupied

### Logs
- Backend logs appear in terminal where `run.py` is running
- Frontend logs in React Native debugger

## 📄 License

This project is for educational and demonstration purposes.

---

**⚕️ Remember: This tool provides general health information only. Always consult qualified healthcare professionals for medical advice, diagnosis, or treatment.**


**⚠️⚠️NOTICE: Operational Status & Strategic Pivot:“While the core prototype was successfully built, further production deployment, live hosting, and multi-platform scaling were intentionally paused. As an independent, solo developer, the compounding challenges of personal financial constraints for hosting architecture, the structural isolation of working without a technical co-founder, and the critical need to prioritize my Class 12 board examinations required a strategic pause on development.”**