# ==============================
# Imports
# ==============================
from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader


# ==============================
# Financial Document Reader Tool
# ==============================
class FinancialDocumentTool:

    @tool("Read Financial Document")
    def read_data_tool(path: str = "data/sample.pdf") -> str:
        """
        Reads a financial PDF document from the given path
        and returns cleaned text content.
        """

        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""

        for data in docs:
            content = data.page_content

            # Remove extra blank lines
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        return full_report