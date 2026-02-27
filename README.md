# 📊 AI Financial Document Analyzer

# 🚀 Project Overview

This project is a financial document analyzer built using:

-   FastAPI -- API layer\
-   CrewAI -- Multi-agent document analysis\
-   Redis -- Message broker\
-   Celery -- Background task processing\
-   LiteLLM/OpenAI API -- LLM integration

The original repository contained: - Deterministic bugs\
- Inefficient prompts\
- Blocking request architecture

This submission includes: - Fully working backend\
- Fixed task registration issues\
- Optimized prompt flow\
- Async background processing with Celery\
- Proper error handling

------------------------------------------------------------------------

# Bugs Identified & Fixes

## 1️⃣ Inefficient Prompts

### ❌ Problem

Original prompts were verbose, unstructured, and inconsistent.

### ✅ Improvements

-   Structured financial analysis roles
-   Clear output expectations
-   Reduced unnecessary verbosity
-   Improved determinism in responses

------------------------------------------------------------------------

## 2️⃣ Celery Task Not Registered

### Issue

Received unregistered task of type 'tasks.analyze_document_task'

### Fix

Updated celery_app.py to explicitly import tasks:

``` python
from celery import Celery

celery_app = Celery(
    "financial_analyzer",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

import tasks  # Explicit import to register tasks
```

------------------------------------------------------------------------

## 3️⃣ Blocking API Execution

### Issue

Financial analysis was running synchronously, causing long response
times.

### Fix

Integrated Redis + Celery for background task processing.

New Flow:

Client → FastAPI → Redis Queue → Celery Worker → Redis Result → Client
Polling

------------------------------------------------------------------------

## 4️⃣ Error Handling Improvements

-   Added structured error handling for OpenAI API failures\
-   Prevented server crashes due to quota errors\
-   Implemented task status tracking

------------------------------------------------------------------------

# ⚡ Bonus Implementation

## ✅ Queue Worker Model (Implemented)

Upgraded system to handle concurrent requests using:

-   Redis as message broker\
-   Celery as background worker\
-   Async result polling endpoint

Benefits: - Non-blocking API\
- Supports multiple simultaneous uploads\
- Scalable architecture

------------------------------------------------------------------------

# 🏗 System Architecture

User\
↓\
FastAPI (/analyze)\
↓\
Redis Queue\
↓\
Celery Worker\
↓\
CrewAI + LLM\
↓\
Redis Result Backend\
↓\
FastAPI (/result/{task_id})

------------------------------------------------------------------------

# 🛠 Setup Instructions

## 1️⃣ Clone Repository

``` bash
git clone <your_repo_link>
cd financial-document-analyzer
```

## 2️⃣ Create Virtual Environment

``` bash
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

## 4️⃣ Run Redis (Docker)

``` bash
docker run -d -p 6379:6379 --name redis-server redis
docker ps
```

## 5️⃣ Set OpenAI API Key

``` bash
setx OPENAI_API_KEY "your_api_key_here"
```

Restart terminal after setting.

## 6️⃣ Start Celery Worker

``` bash
celery -A celery_app.celery_app worker --pool=solo --loglevel=info
```

You should see:

\[tasks\] . tasks.analyze_document_task

## 7️⃣ Start FastAPI Server

Keep celery terminal open and open another terminal and run the following
``` bash
uvicorn main:app --reload
```

Open in browser:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# 📘 API Documentation

## POST /analyze

Uploads financial document and starts background analysis.

Response:

``` json
{
  "status": "processing",
  "task_id": "uuid",
  "message": "Analysis started in background"
}
```

------------------------------------------------------------------------

## GET /result/{task_id}

Returns analysis result.

Success:

``` json
{
  "status": "completed",
  "result": "Analysis output..."
}
```

Failure:

``` json
{
  "status": "failed",
  "error": "Error details"
}
```

------------------------------------------------------------------------

# 📈 Improvements Summary

✔ Fixed deterministic bugs\
✔ Improved prompt quality\
✔ Implemented async queue model\
✔ Enabled concurrent request handling\
✔ Added structured error handling\
✔ Made system scalable



