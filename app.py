import streamlit as st
import os
import tempfile
from backend.core.auditor import FinancialAuditor
from backend.core.orchestrator import AuditOrchestrator
from backend.eval.evaluator import RAGASEvaluator

# --- Page Configuration ---
st.set_page_config(
    page_title="Financial Intelligence Audit Suite",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Aesthetics ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Card/Glassmorphism */
    .audit-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Title Styling */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'auditor' not in st.session_state:
    st.session_state.auditor = FinancialAuditor()
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = AuditOrchestrator()
if 'evaluator' not in st.session_state:
    st.session_state.evaluator = RAGASEvaluator()
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Sidebar: Document Management ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/data-configuration.png", width=80)
    st.markdown("### Evidence Vault")
    uploaded_files = st.file_uploader(
        "Ingest Financial Documents", 
        type=['pdf', 'png', 'jpg', 'jpeg', 'csv', 'xlsx'], 
        accept_multiple_files=True
    )
    
    # Auto-indexing when files are uploaded
    if uploaded_files:
        if 'last_indexed_count' not in st.session_state or st.session_state.last_indexed_count != len(uploaded_files):
            progress_bar = st.progress(0)
            status_text = st.empty()
            with st.spinner("Executing High-Precision Indexing..."):
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.markdown(f"**Analyzing:** `{uploaded_file.name}`")
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    st.session_state.orchestrator.ingest_file(tmp_path)
                    os.unlink(tmp_path)
                    progress_bar.progress((i + 1) / len(uploaded_files))
            st.session_state.last_indexed_count = len(uploaded_files)
            status_text.markdown("✅ **Evidence Secured.** High-precision vault active.")

    st.markdown("---")
    st.markdown("#### Forensic Guardrails")
    st.info("Accuracy: MAX\n\nVerification: Multi-Pass active\n\nStandards: IFRS / GAAP")

    st.markdown("---")
    st.markdown("#### System Status")
    st.info("Role: Senior AI Auditor\n\nStandards: IFRS / GAAP\n\nMode: Multi-modal RAG")

# --- Main Interface ---
st.markdown('<h1 class="main-title">Financial Intelligence Audit Suite</h1>', unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>Forensic-grade analysis and multi-modal reconciliation.</p>", unsafe_allow_html=True)

# Audit Query Input
with st.container():
    st.markdown('<div class="audit-card">', unsafe_allow_html=True)
    query = st.text_area("Enter Audit Query (e.g., 'Compare EBITDA margins across these reports and highlight variances')", placeholder="Type your forensic inquiry here...")
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        run_audit = st.button("Execute Audit", type="primary")
    with col2:
        if st.button("Cancel"):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Audit Results
if run_audit:
    if not query.strip():
        st.error("⚠️ **Input Error:** Please enter a valid audit query to execute analysis.")
    else:
        with st.spinner("Analyzing context and performing forensic checks..."):
            try:
                # 1. Get raw evidence for transparency
                evidence_data = st.session_state.orchestrator.query(query)
                contexts = evidence_data.get("documents", [[]])[0]
                
                # 2. Run analysis
                analysis = st.session_state.auditor.analyze(query)
                
                # 3. Evaluate with RAGAS
                with st.spinner("Calculating Forensic Quality Scores..."):
                    scores = st.session_state.evaluator.evaluate_engagement(
                        query, analysis, contexts
                    )
                
                st.session_state.history.append({
                    "query": query, 
                    "result": analysis,
                    "evidence": contexts,
                    "scores": scores
                })
            except Exception as e:
                st.error(f"⚠️ **Audit Interruption:** The forensic engine encountered an issue. Details: {str(e)}")

if st.session_state.history:
    for i, entry in enumerate(reversed(st.session_state.history)):
        idx = len(st.session_state.history) - i
        st.markdown(f"### Audit Engagement {idx}")
        
        # Display Scores
        scores = entry.get("scores", {})
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Faithfulness (Accuracy)", f"{scores.get('faithfulness', 0):.2f}")
        with col2:
            # Handle both naming conventions
            rel_score = scores.get('answer_relevance') or scores.get('answer_relevancy') or 0
            st.metric("Answer Relevance", f"{rel_score:.2f}")
            
        st.markdown(entry["result"])
        
        with st.expander(f"🔍 View Evidence Snippets for Engagement {idx}"):
            for snippet in entry.get("evidence", []):
                st.info(f"```text\n{snippet}\n```")
        st.markdown('<div class="audit-card">', unsafe_allow_html=True)
        st.markdown(f"**Query:** {entry['query']}")
        st.markdown("---")
        st.markdown(entry['result'])
        st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Developed by Antigravity | Senior Financial AI Auditor Suite v1.0</p>", unsafe_allow_html=True)
