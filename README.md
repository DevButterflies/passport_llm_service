
# 🛂 Passport Field Extraction API

A high-performance FastAPI service that utilizes LLM APIs (Gemini) to extract structured data from passport images. The system includes built-in rate limiting, detailed request logging, and comprehensive audit trails for API performance tracking.

## 🚀 Features
- **LLM Integration:** Powered by Gemini for high-accuracy OCR and field mapping.
- **Robust Logging:** Automatic request/response logging with file rotation.
- **Rate Limiting:** Integrated `slowapi` to prevent API abuse.
- **Audit System:** Tracks token usage, model latency, and API key rotations.
- **Health Monitoring:** Dedicated `/health` endpoint for container orchestration.

---

## 🛠️ Tech Stack
- **Backend:** FastAPI
- **LLM API:** Google Gemini (Flash Lite)
- **Rate Limiting:** SlowAPI
- **Server:** Uvicorn
- **Environment:** Docker + WSL2

---

## 📋 Prerequisites
- Python 3.10+
- Docker Desktop (Installed & Running)
- VS Code (with Docker Extension)
- Gemini API Key

---

## ⚙️ Configuration
The application relies on an `app/config.py` file. Ensure you have your environment variables set up:
- `HOST`: Server host (e.g., `0.0.0.0`)
- `PORT`: Server port (e.g., `8001`)
- `LOGS_PATH`: Path to save log files (e.g., `./logs/app.log`)

---

## 🏃 Step-by-Step Execution

### 1. Local Setup
First, clone your project and set up a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running Locally
Run the application using the module flag:
```bash
python -m app.main
```
The API will be available at `http://localhost:8001`.

## 🧪 API Usage

### Extract Passport Data
**Endpoint:** `POST /passport_card`  
**Payload:** `multipart/form-data`  
**Field:** `photo` (Image file)

#### Example Request (cURL):
```bash
curl -X POST http://localhost:8001/passport_card \
  -F "photo=@/path/to/your/passport_image.jpg"
```

#### Example Response:
```json
{
    "data": {
        "country_code": "TUN",
        "passport_number": "H801892",
        "date_of_birth": "1992-01-26",
        "expiration_date": "2026-12-27",
        "nationality": "TUN",
        "sex": "M",
        "given_names": "MARWEN",
        "surname": "BEN HSSIN",
        "personal_number": "12805788"
    },
    "audit": {
        "model": "gemini-3.1-flash-lite-preview",
        "total_input_tokens": 518.0,
        "total_output_tokens": 30.0,
        "duration_total": 41.60
    },
    "duration": "41.64"
}
```

---

## 📁 Project Structure
```text
├── app/
│   ├── main.py          # Entry point (FastAPI initialization)
│   ├── api/
│   │   └── router.py    # Route definitions
│   ├── config.py        # Environment configurations
│   └── ...              # LLM logic and helpers
├── logs/                # Automatically created logs folder
├── Dockerfile           # Docker configuration
└── requirements.txt     # Python dependencies
```

---

## 🛡️ Health Check
Monitor the service status at:
`GET http://localhost:8001/health`
