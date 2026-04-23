import os
from typing import List, Dict, Any
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_google_genai import ChatGoogleGenerativeAI
from datasets import Dataset
from dotenv import load_dotenv

load_dotenv()

class RAGASEvaluator:
    """
    Automated Forensic Quality Assessment using RAGAS + Gemini (Free).
    Measures Faithfulness and Relevance of audit findings.
    """
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        # Gemini-1.5-Flash is excellent and free for evaluation
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=self.api_key
        )

    def evaluate_engagement(self, question: str, answer: str, contexts: List[str]) -> Dict[str, float]:
        """
        Calculates RAGAS metrics for a single forensic engagement.
        """
        data = {
            "question": [question],
            "answer": [answer],
            "contexts": [contexts]
        }
        dataset = Dataset.from_dict(data)
        
        # Run evaluation
        try:
            result = evaluate(
                dataset,
                metrics=[faithfulness, answer_relevancy],
                llm=self.llm,
                raise_exception=False
            )
            return result.to_pandas().iloc[0].to_dict()
        except Exception as e:
            print(f"[!] RAGAS Evaluation Failed: {e}")
            return {"faithfulness": 0.0, "answer_relevance": 0.0}

if __name__ == "__main__":
    # Test evaluation
    evaluator = RAGASEvaluator()
    q = "What is the revenue?"
    a = "The revenue is $10M"
    ctx = ["Revenue reported in Q3 is $10M."]
    scores = evaluator.evaluate_engagement(q, a, ctx)
    print(f"Audit Quality Scores: {scores}")
