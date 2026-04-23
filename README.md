# ⚖️ Financial Intelligence Audit Suite

A forensic-grade RAG (Retrieval-Augmented Generation) system designed for deep financial analysis, mathematical reconciliation, and automated compliance auditing.

---

## 🚀 Simplified Forensic Audit Flow

```mermaid
graph LR
    USER((User)) -- "1" --> PC[Streamlit Console]
    PC -- "2" --> RET[Audit Orchestrator]
    RET -- "3" --> DB[(Evidence Vault)]
    DB -- "4" --> RET
    RET -- "5" --> LLM{Gemini 1.5 Flash}
    LLM -- "6" --> RET
    RET -- "7" --> PC
```

### 📁 Data Flow Breakdown

| Step | Direction | Component Path | Explanation |
| :--- | :--- | :--- | :--- |
| **1** | **Inflow** | User → Console | The user submits a financial query or audit request via the UI. |
| **2** | **Inflow** | Console → Orchestrator | The UI captures the request and triggers the backend analytical pipeline. |
| **3** | **Outflow** | Orchestrator → Vault | The system converts your query into a "meaning" code and searches the database. |
| **4** | **Inflow** | Vault → Orchestrator | The most relevant evidence snippets are retrieved from the stored documents. |
| **5** | **Outflow** | Orchestrator → LLM | The raw query + retrieved evidence are combined into a high-fidelity audit prompt. |
| **6** | **Inflow** | LLM → Orchestrator | The AI performs a multi-pass verification and returns a reconciled forensic report. |
| **7** | **Outflow** | Orchestrator → Console | The final verified answer is delivered to the dashboard for the user to review. |

---

## 🏛️ Strategic System Design (Enterprise View)

```mermaid
flowchart TD
    subgraph UI ["<b>User Interface Layer</b>"]
        direction LR
        UQ["User Audit Query"]
        RTU["Verified Audit Report"]
    end

    subgraph LLM_ENGINE ["<b>Forensic Analytical Engine</b>"]
        direction TB
        EX["Context Extraction"]
        RAG["Forensic RAG Loop"]
        SUCCESS{Evidence <br/>Found?}
        GUARD["CoVe Verification Guardrail"]
        GOOD{Accuracy <br/>Verified?}
        JUDGE["Judicial AI (RAGAS)"]
    end

    subgraph DATA ["<b>Evidence & Meta Data</b>"]
        direction TB
        CC["Document Context"]
        KB[("Forensic Vault <br/>(Chroma / Azure)")]
    end

    subgraph FEEDBACK ["<b>Verification & Improvements</b>"]
        direction LR
        REV["Human Auditor Review"]
        ENG["Forensic Pattern Learning"]
    end

    %% Flow Relationships
    UQ --> EX
    CC --> EX
    EX --> RAG
    KB <--> RAG
    RAG --> SUCCESS
    
    SUCCESS -- Yes --> GUARD
    SUCCESS -- No --> REV
    
    GUARD --> GOOD
    GOOD -- Yes --> RTU
    GOOD -- No --> REV
    
    RTU --> JUDGE
    JUDGE --> ENG
    ENG --> KB
```

---

## 🏗️ System Architecture Design

```mermaid
graph LR
    subgraph "User Tier"
        UI["Streamlit Dashboard"]
    end

    subgraph "Logic Tier (Orchestrator)"
        ORCH["Audit Orchestrator"]
        LOAD["Multi-Modal Loader"]
        SPLIT["Recursive Splitter"]
    end

    subgraph "AI & Intelligence Tier"
        GEM_LLM["Gemini 1.5 Flash <br/><i>(Reasoning & CoVe)</i>"]
        GEM_EMB["Gemini Embedding <br/><i>(Vectorization)</i>"]
        RAGAS["RAGAS Evaluator <br/><i>(Judicial Scoring)</i>"]
    end

    subgraph "Data Tier (Hybrid)"
        CHROMA[("ChromaDB <br/><i>Local Storage</i>")]
        AZURE[("Azure AI Search <br/><i>Cloud Hybrid</i>")]
    end

    %% Relationships
    UI <--> ORCH
    ORCH --> LOAD
    LOAD --> SPLIT
    ORCH <--> GEM_EMB
    ORCH <--> GEM_LLM
    GEM_LLM <--> RAGAS
    
    ORCH <--> CHROMA
    ORCH <--> AZURE
```

---

## 🗺️ End-to-End Forensic Workflow

```mermaid
graph TD
    subgraph "Phase 1: Multi-Modal Ingestion"
        A[User Uploads Documents] --> B{File Type?}
        B -- PDF/Image --> C[PyMuPDF / OCR Extraction]
        B -- Excel/CSV --> D[Pandas Structured Loading]
        C --> E[Recursive Text Chunking]
        D --> E
        E --> F["Gemini Embedding Engine <br/><i>(gemini-embedding-001)</i>"]
        F --> G[(Forensic Vault: Chroma / Azure)]
    end

    subgraph "Phase 2: Hybrid Retrieval"
        H[User Audit Query] --> I["Gemini Query Vectorization <br/><i>(gemini-embedding-001)</i>"]
        I --> J{Search Mode?}
        J -- Local --> K[Vector Similarity Search]
        J -- Azure --> L[Hybrid Keyword + Vector Search]
        L --> M[Semantic Reranking]
        K --> N[Evidence Snippets]
        M --> N
    end

    subgraph "Phase 3: Max-Precision Analysis"
        N --> O["Multi-Pass Verification Loop <br/><i>(Gemini 1.5 Flash)</i>"]
        O --> P[Internal Data Extraction]
        P --> Q[Source-Cross-Reconciliation]
        Q --> R[Final Verified Report]
    end

    subgraph "Phase 4: Quality Assurance"
        R --> S["RAGAS Evaluation Engine <br/><i>(Gemini 1.5 Flash Judge)</i>"]
        S --> T[Faithfulness & Relevance Scores]
        T --> U[Final Audit Dashboard]
    end
```

---

## 🏗️ Component Architecture (Layman's Perspective)

### 1. The Interactive Dashboard (Frontend)
*   **Tech Stack**: [Streamlit](https://streamlit.io/) (Python)
*   **Layman Explanation**: This is the "Face" of the system. It’s like a professional website designed specifically for data. It handles your file uploads and displays the AI's reports in a clean, readable format.

### 2. The Senior Auditor (Analytical Engine)
*   **Tech Stack**: [Google Gemini 1.5 Flash](https://deepmind.google/technologies/gemini/)
*   **Layman Explanation**: This is the "Brain." It has been trained on trillions of words and understands complex accounting rules (IFRS/GAAP). We use a **Chain-of-Verification (CoVe)** process, meaning the AI doesn't just answer; it internally cross-checks its own math before showing you the result.

### 3. The Digital Vault (Vector Memory)
*   **Tech Stack**: [ChromaDB](https://www.trychroma.com/) (Local) or [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search) (Enterprise)
*   **Layman Explanation**: This is the "Memory." Instead of searching for keywords like a 90s search engine, it stores the *meaning* of your documents as mathematical codes. This allows the AI to find relevant context (e.g., "revenue growth") even if the document uses different words like "increased turnover."

### 4. The Document Reader (Multimodal Loader)
*   **Tech Stack**: [PyMuPDF](https://pymupdf.readthedocs.io/), [Pandas](https://pandas.pydata.org/), [PIL](https://python-pillow.org/)
*   **Layman Explanation**: These are the "Eyes." They read messy PDFs, scan images for text, and parse through giant Excel spreadsheets, converting them into a format the AI can analyze.

### 5. The Quality Inspector (Evaluation Framework)
*   **Tech Stack**: [RAGAS](https://docs.ragas.io/)
*   **Layman Explanation**: This is the "Supervisor." For every answer the AI gives, RAGAS runs a background check to ensure it is **Faithful** (didn't make up numbers) and **Relevant** (actually answered your question).

---

## 🚀 Key Features
*   **Forensic Verification**: Mandatory multi-pass internal reconciliation of numerical data.
*   **Hybrid Search**: Combines keyword precision with semantic meaning (when using Azure).
*   **Auto-Indexing**: Zero-click document ingestion pipeline.
*   **Hallucination Shield**: Strict citation protocol for every claim.

## 🛠️ Setup & Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env`:
   * `GOOGLE_API_KEY`: Required for the Brain and Memory.
   * `AZURE_SEARCH_API_KEY`: Optional for Enterprise search.
4. Run the suite: `streamlit run app.py`
