from celery_app import celery_app
from crew_runner import run_crew
import os

@celery_app.task
def analyze_document_task(file_path: str, query: str):

    result = run_crew(query=query, file_path=file_path)

    # Optional cleanup AFTER analysis
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            pass

    return str(result)