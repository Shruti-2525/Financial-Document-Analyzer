from fastapi import FastAPI, File, UploadFile, Form
from celery.result import AsyncResult
from celery_app import celery_app
from tasks import analyze_document_task

import os
import uuid
from crew_runner import run_crew

# # CrewAI imports
# from crewai import Crew, Process
# from agents import financial_analyst
# from task import analyze_financial_document as financial_analysis_task

# app = FastAPI(title="Financial Document Analyzer")


# # ==============================
# # Crew Runner Function
# # ==============================
# def run_crew(query: str, file_path: str = "data/sample.pdf"):
#     """Runs the CrewAI financial analysis workflow"""

#     financial_crew = Crew(
#         agents=[financial_analyst],
#         tasks=[financial_analysis_task],
#         process=Process.sequential,
#     )

#     result = financial_crew.kickoff({
#         "query": query,
#         "file_path": file_path
#     })

#     return result


# ==============================
# Check Task Result Endpoint
# ==============================
app = FastAPI(title="Financial Document Analyzer")
@app.get("/result/{task_id}")
def get_result(task_id: str):

    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == "PENDING":
        return {"status": "pending"}

    if task_result.state == "SUCCESS":
        return {
            "status": "completed",
            "result": task_result.result
        }

    if task_result.state == "FAILURE":
        return {
            "status": "failed",
            "error": str(task_result.info)
        }

    return {"status": task_result.state}
@app.get("/")
def root():
    return {"message": "Financial Document Analyzer API is running"}


# ==============================
# Analyze Endpoint (Async)
# ==============================
@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document asynchronously using Celery"""

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate query
        if not query:
            query = "Analyze this financial document for investment insights"

        #  Send task to Celery background worker
        task = analyze_document_task.delay(
            file_path=file_path,
            query=query.strip()
        )

        return {
            "status": "processing",
            "task_id": task.id,
            "message": "Analysis started in background",
            "file_processed": file.filename
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }