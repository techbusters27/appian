import streamlit as st
import time
from simple_vector_store import LocalKnowledgeBase, load_dummy_data

# Page Config
st.set_page_config(page_title="Appian Just-in-Time Knowledge", layout="wide")

# Initialize Knowledge Base (Cached)
@st.cache_resource
def get_knowledge_base():
    kb = LocalKnowledgeBase()
    load_dummy_data(kb)
    return kb

kb = get_knowledge_base()

# CUSTOM CSS FOR THEMING
st.markdown("""
<style>
    /* Appian-inspired Blue & Clean Theme */
    .stApp {
        background-color: #eff6ff;
    }
    h1, h2, h3 {
        color: #1d3557;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    /* Card Styling */
    .result-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        border-left: 5px solid #2563eb;
    }
    .result-score {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .source-link {
        color: #2563eb;
        text-decoration: none;
        font-weight: 500;
    }
    .source-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("🛡️ Appian Intelligent Case Management")
st.markdown("___")

# MAIN LAYOUT
# Using container for better responsiveness
with st.container():
    col1, col2 = st.columns([1.5, 1], gap="medium")

    # LEFT COLUMN: CASE CONTEXT
    with col1:
        st.subheader("📝 Active Case Details")
        
        with st.form("claim_form"):
            st.markdown("**Claim Information**")
            c1, c2 = st.columns(2)
            with c1:
                claim_id = st.text_input("Claim ID", "CLM-2024-001")
                claim_type = st.selectbox("Claim Type", ["Auto", "Home", "Liability"])
            with c2:
                claim_state = st.selectbox("Jurisdiction", ["FL (Florida)", "NY (New York)", "CA (California)"])
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                
            incident_description = st.text_area("Incident Description", 
                "Customer reported water damage due to a burst pipe during the hurricane. Policy holder is asking if flood damage is covered.", height=100)
            
            submitted = st.form_submit_button("Update Case & Fetch Policies")

    # RIGHT COLUMN: KNOWLEDGE ASSISTANT
    with col2:
        st.subheader("💡 Knowledge Assistant")
        
        # Placeholder for "Assistant is thinking"
        assistant_container = st.empty()
        
        if submitted or incident_description:
            # Construct Query
            query = f"{claim_type} policy regarding {incident_description} in {claim_state}"
            
            with st.spinner("🤖 AI is analyzing case context..."):
                time.sleep(0.6) # UX: Simulate thinking
                results = kb.search(query, top_k=2)
            
            if results:
                for r in results:
                    chunk = r["chunk"]
                    meta = chunk["metadata"]
                    score = r["score"]
                    
                    # HTML Card for better aesthetics
                    st.markdown(f"""
                    <div class="result-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:bold; font-size:1.1rem;">📄 {meta['doc_name']}</span>
                            <span class="result-score">Match: {int(score*100)}%</span>
                        </div>
                        <div style="color:#64748b; font-size:0.9rem; margin-top:0.2rem;">
                            Page {meta.get('page', '?')} • Paragraph {meta.get('paragraph', 1)}
                        </div>
                        <p style="margin-top:0.8rem; color:#374151; font-style:italic;">
                            "{chunk['text'].strip()}..."
                        </p>
                        <div style="margin-top:1rem; text-align:right;">
                            <a href="{meta['url']}" target="_blank" class="source-link">🔗 Open Verified Source</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No specific policy guidelines found for this scenario.")
        else:
            assistant_container.info("👈 Update the case form to see proactive suggestions.")

st.markdown("___")
st.caption("Appian Proactive Knowledge Demo | Powered by SentenceTransformers | v2.0")

# SIDEBAR: Knowledge Management
with st.sidebar:
    st.header("📚 Knowledge Base")
    st.info("Upload your own policy documents (PDF) to the brain.")
    
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Ingest Document"):
            import pypdf
            
            with st.spinner("Reading PDF..."):
                reader = pypdf.PdfReader(uploaded_file)
                text_content = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        # Add each page as a "Chunk" or slightly larger segment
                        # For this simple demo, we pass page-by-page to the chunker
                        kb.add_document(
                            text=page_text, 
                            metadata={
                                "doc_name": uploaded_file.name, 
                                "page": page_num + 1, 
                                "url": f"http://internal-docs/{uploaded_file.name}"
                            }
                        )
                
                # Re-build index with new data
                kb.build_index()
                st.success(f"Successfully ingested '{uploaded_file.name}'!")
                st.balloons()

