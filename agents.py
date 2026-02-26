# ==============================
# Importing Libraries
# ==============================
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools import FinancialDocumentTool

# ==============================
# Load Environment Variables
# ==============================
load_dotenv()

# ==============================
# Validate API Key
# ==============================
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# ==============================
# Initialize LLM
# ==============================
llm = LLM(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=api_key
)

# ==============================
# Financial Analyst Agent
# ==============================
financial_analyst = Agent(
    role="Senior Financial Analyst",

    goal=(
        "Provide accurate, structured, and evidence-based financial analysis "
        "strictly based on the uploaded financial document and the user query: {query}."
    ),

    backstory=(
        "You are a CFA-certified financial analyst with over 15 years of experience "
        "in corporate finance, equity research, and investment strategy. "
        "You specialize in analyzing annual reports, quarterly earnings, "
        "balance sheets, income statements, and cash flow statements. "
        "You never fabricate data and only use verified information from the document."
    ),

    verbose=True,
    memory=True,
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=5,
    allow_delegation=False
)