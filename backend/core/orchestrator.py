import os
import uuid
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.loaders.multimodal_loader import MultiModalFinancialLoader
from backend.vector_store.chroma_manager import FinancialVectorStore
from backend.vector_store.azure_search_manager import AzureSearchManager
from dotenv import load_dotenv

load_dotenv()

class AuditOrchestrator:
    """
    Orchestrates the flow from raw file ingestion to enterprise vector indexing.
    """
    def __init__(self):
        self.loader = MultiModalFinancialLoader()
        
        # Determine if we use Azure or Local ChromaDB
        self.use_azure = os.getenv("AZURE_SEARCH_API_KEY") is not None
        if self.use_azure:
            print("[*] Initializing Enterprise Azure AI Search Engine...")
            self.vector_store = AzureSearchManager()
        else:
            print("[*] Initializing Local Forensic Vector Vault...")
            self.vector_store = FinancialVectorStore()
            
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150,
            separators=["\n\n", "\n", " ", ""]
        )

    def ingest_file(self, file_path: str, deep_scan: bool = False):
        """
        Processes a file and stores it in the chosen vector vault.
        """
        print(f"[*] Ingesting: {file_path} (Deep Scan: {deep_scan})")
        
        extracted_data = self.loader.load_document(file_path, deep_scan=deep_scan)
        raw_text = extracted_data.get("text", "")
        metadata = extracted_data.get("metadata", {})
        
        chunks = self.text_splitter.split_text(raw_text)
        
        if self.use_azure:
            print(f"[*] Enterprise Vectorizing {len(chunks)} chunks...")
            azure_docs = []
            # We use the Chroma manager's embedding fn logic to keep it free
            # Accessing it via a temp instance or better, defining it in a shared place.
            from backend.vector_store.chroma_manager import BatchGeminiEmbeddingFunction
            embed_fn = BatchGeminiEmbeddingFunction(api_key=os.getenv("GOOGLE_API_KEY"))
            
            vectors = embed_fn(chunks)
            for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
                azure_docs.append({
                    "id": str(uuid.uuid4()).replace("-", ""), # Azure IDs can't have hyphens in some configs
                    "content": chunk,
                    "content_vector": vector,
                    "metadata": str(metadata),
                    "source": os.path.basename(file_path)
                })
            self.vector_store.add_documents(azure_docs)
        else:
            chunk_metadatas = [metadata for _ in chunks]
            chunk_ids = [str(uuid.uuid4()) for _ in chunks]
            self.vector_store.add_documents(texts=chunks, metadatas=chunk_metadatas, ids=chunk_ids)

    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Retrieves relevant forensic context. Supports Azure Hybrid/Semantic search.
        """
        if self.use_azure:
            from backend.vector_store.chroma_manager import BatchGeminiEmbeddingFunction
            embed_fn = BatchGeminiEmbeddingFunction(api_key=os.getenv("GOOGLE_API_KEY"))
            query_vector = embed_fn([user_query])[0]
            return self.vector_store.query(user_query, vector=query_vector, n_results=10)
        return self.vector_store.query(user_query, n_results=10)

    def query_audit_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for relevant evidence across all ingested documents.
        """
        results = self.vector_store.query(query)
        
        # Format results for the Auditor Persona
        formatted_results = []
        if results and 'documents' in results:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        return formatted_results

if __name__ == "__main__":
    # Test initialization
    orchestrator = AuditOrchestrator()
    print("Audit Orchestrator ready.")
