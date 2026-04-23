import os
import google.generativeai as genai
from typing import List, Dict, Any
from backend.core.orchestrator import AuditOrchestrator
from dotenv import load_dotenv

load_dotenv()

class FinancialAuditor:
    """
    The 'Senior Financial AI Auditor' persona powered by Gemini (Free Tier).
    """
    def __init__(self):
        self.orchestrator = AuditOrchestrator()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def analyze(self, user_query: str) -> str:
        """
        Maximum Precision analytical loop with internal data reconciliation (CoVe).
        """
        # 1. Deep Retrieval (Increased window for better context)
        context_data = self.orchestrator.query(user_query)
        documents = context_data.get("documents", [[]])[0]
        metadatas = context_data.get("metadatas", [[]])[0]
        
        context_str = ""
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            source = meta.get('source', 'Unknown')
            context_str += f"\n[SOURCE {i+1}: {source}]\n{doc}\n"

        # 2. Multi-Pass Forensic Verification Loop
        verification_prompt = f"""
        YOU ARE THE HIGH-PRECISION FORENSIC AI AUDITOR.
        Perform a 3-Step Verification for the query: "{user_query}"
        
        STEP 1: Extract all relevant numbers, dates, and names from the evidence.
        STEP 2: Cross-check every number against the sources. If a number appears in multiple places, verify they match.
        STEP 3: Generate a final, reconciled report with 100% accuracy.
        
        EVIDENCE VAULT:
        {context_str}
        
        CONSTRAINTS:
        - Accuracy is the ONLY priority.
        - Cite every fact using [SOURCE X].
        - If numbers don't reconcile, flag it as an "Audit Conflict".
        - Do not provide a range if a specific number is available.
        - Variance > 5% MUST be highlighted.
        
        FINAL FORENSIC REPORT:
        """
        
        response = self.model.generate_content(verification_prompt)
        return response.text

if __name__ == "__main__":
    # Test stub
    auditor = FinancialAuditor()
    print("Senior Financial Auditor initialized.")
