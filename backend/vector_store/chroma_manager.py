import chromadb
from chromadb.utils import embedding_functions
import os
import time
import google.generativeai as genai
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class BatchGeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
    """
    Custom embedding function that utilizes Gemini's native batch endpoint
    for 100x faster processing of large document sets.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)

    def __call__(self, input: List[str]) -> List[List[float]]:
        # Gemini allows up to 100 texts per batch
        batch_size = 100
        embeddings = []
        
        for i in range(0, len(input), batch_size):
            batch = input[i:i + batch_size]
            try:
                result = genai.embed_content(
                    model="models/gemini-embedding-2-preview",
                    content=batch,
                    task_type="retrieval_document"
                )
                embeddings.extend(result['embedding'])
            except Exception as e:
                print(f"[*] Embedding Error: {e}. Retrying...")
                time.sleep(2)
                # Simple retry logic
                result = genai.embed_content(
                    model="models/gemini-embedding-2-preview",
                    content=batch,
                    task_type="retrieval_document"
                )
                embeddings.extend(result['embedding'])
                
        return embeddings

class FinancialVectorStore:
    """
    Manages the persistent vector database with high-speed batch embedding.
    """
    def __init__(self, collection_name: str = "audit_suite_v3"):
        self.db_path = os.getenv("CHROMA_DB_PATH", "./data/vector_store")
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        self.api_key = os.getenv("GOOGLE_API_KEY")
        # Use our high-speed custom batch embedder
        self.embedding_fn = BatchGeminiEmbeddingFunction(api_key=self.api_key)
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """
        Adds documents using the optimized batch function.
        """
        # ChromaDB will call our __call__ method which handles the 100-chunk batching
        try:
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
        except Exception as e:
            print(f"[!] Critical Indexing Error: {e}")
            raise e

    def query(self, query_text: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Performs semantic search with error handling.
        """
        try:
            return self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
        except Exception as e:
            print(f"[!] Query Error: {e}")
            return {}

    def delete_collection(self):
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            embedding_function=self.embedding_fn
        )

if __name__ == "__main__":
    # Test initialization
    v_store = FinancialVectorStore()
    print(f"Vector Store initialized at {v_store.db_path}")
