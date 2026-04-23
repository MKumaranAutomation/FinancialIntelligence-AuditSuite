import os
from typing import List, Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch
)
from dotenv import load_dotenv

load_dotenv()

class AzureSearchManager:
    """
    Enterprise-grade Forensic Search using Azure AI Search (Hybrid + Semantic).
    """
    def __init__(self, index_name: str = "audit-suite-index"):
        self.endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
        self.key = os.getenv("AZURE_SEARCH_API_KEY")
        self.index_name = index_name
        
        self.credential = AzureKeyCredential(self.key)
        self.index_client = SearchIndexClient(endpoint=self.endpoint, credential=self.credential)
        self.search_client = SearchClient(endpoint=self.endpoint, index_name=self.index_name, credential=self.credential)
        
        # Ensure Index Exists
        self._create_index_if_not_exists()

    def _create_index_if_not_exists(self):
        try:
            self.index_client.get_index(self.index_name)
        except Exception:
            # Define Forensic Index Schema
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
                SearchField(name="content_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                            searchable=True, vector_search_dimensions=768, vector_search_profile_name="audit-vector-profile"),
                SimpleField(name="metadata", type=SearchFieldDataType.String),
                SimpleField(name="source", type=SearchFieldDataType.String, filterable=True, facetable=True)
            ]
            
            vector_search = VectorSearch(
                profiles=[VectorSearchProfile(name="audit-vector-profile", algorithm_configuration_name="audit-hnsw")],
                algorithms=[HnswAlgorithmConfiguration(name="audit-hnsw")]
            )
            
            semantic_search = SemanticSearch(configurations=[
                SemanticConfiguration(
                    name="audit-semantic-config",
                    prioritized_fields=SemanticPrioritizedFields(
                        content_fields=[SemanticField(field_name="content")]
                    )
                )
            ])
            
            index = SearchIndex(
                name=self.index_name,
                fields=fields,
                vector_search=vector_search,
                semantic_search=semantic_search
            )
            self.index_client.create_index(index)
            print(f"[*] Azure AI Search Index '{self.index_name}' created.")

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Uploads forensic documents to the Azure index.
        """
        try:
            self.search_client.upload_documents(documents)
            print(f"[*] Successfully indexed {len(documents)} snippets in Azure.")
        except Exception as e:
            print(f"[!] Azure Indexing Error: {e}")

    def query(self, query_text: str, vector: List[float] = None, n_results: int = 5) -> Dict[str, Any]:
        """
        Executes Hybrid + Semantic Search for Maximum Precision.
        """
        try:
            results = self.search_client.search(
                search_text=query_text,
                vector_queries=[{
                    "value": vector,
                    "fields": "content_vector",
                    "k_nearest_neighbors": n_results
                }] if vector else None,
                query_type="semantic",
                semantic_configuration_name="audit-semantic-config",
                top=n_results
            )
            
            output = {"documents": [[]], "metadatas": [[]]}
            for res in results:
                output["documents"][0].append(res["content"])
                output["metadatas"][0].append({"source": res["source"]})
            return output
        except Exception as e:
            print(f"[!] Azure Search Query Error: {e}")
            return {"documents": [[]], "metadatas": [[]]}
