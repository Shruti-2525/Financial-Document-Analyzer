from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document as financial_analysis_task


def run_crew(query: str, file_path: str):
    """Run the financial analysis crew"""

    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[financial_analysis_task],
        process=Process.sequential,
    )

    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path
    })

    return result