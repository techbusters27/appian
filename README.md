# Walkthrough: Appian Just-in-Time Knowledge Retrieval

I have completed the design and prototyping for the "Just-in-Time" knowledge retrieval system. This solution addresses the "Alt-Tab" problem by proactively pushing context-aware policy documents to agents directly within Appian.

## Solution Architecture

The solution is composed of three main parts:
1.  **The Brain (Ingestion)**: Python script to chunk PDFs and store them with verifiable metadata.
2.  **The Bridge (Integration)**: Appian objects to query the Vector DB based on case context.
3.  **The Assistant (UI)**: A side-panel interface that displays results with deep links to specific pages.

## Artifacts Created

| Component | File | Description |
| :--- | :--- | :--- |
| **Data Schema** | [vector_schema.md](file:///C:/Users/gsjit/.gemini/antigravity/brain/50b619c6-e1fa-4838-87cd-8f2160416e75/vector_schema.md) | Defines metadata for "Verifiable Citations" (pages, paragraphs). |
| **Ingestion** | [knowledge_ingestion.py](file:///C:/Users/gsjit/appian/knowledge_ingestion.py) | Python script to ingest PDFs and upload to Vector DB. |
| **Integration** | [Appian_Integration_Design.md](file:///C:/Users/gsjit/.gemini/antigravity/brain/50b619c6-e1fa-4838-87cd-8f2160416e75/Appian_Integration_Design.md) | Design for Connected System & Integration Object. |
| **User Interface** | [Appian_UI_Components.md](file:///C:/Users/gsjit/.gemini/antigravity/brain/50b619c6-e1fa-4838-87cd-8f2160416e75/Appian_UI_Components.md) | SAIL design for the "Knowledge Assistant" side panel. |
| **Plan** | [implementation_plan.md](file:///C:/Users/gsjit/.gemini/antigravity/brain/50b619c6-e1fa-4838-87cd-8f2160416e75/implementation_plan.md) | Initial technical plan. |

## Verification Results

### Knowledge Ingestion Prototype
I ran the [knowledge_ingestion.py](file:///C:/Users/gsjit/appian/knowledge_ingestion.py) script to simulate the ingestion of an "Auto Claims Policy".

**Command:** `python knowledge_ingestion.py`

**Output:**
```
Initialized Knowledge Engine for index: appian-knowledge
Loading document: Auto_Claims_Policy_v2.pdf
Created 4 chunks from document.
Upserting 4 vectors to Pinecone/Weaviate...
Upsert complete.
```

### Interactive Demo (Streamlit)
I have created a local interactive prototype that simulates the Appian embedded experience.

**Files Created:**
- [simple_vector_store.py](file:///C:/Users/gsjit/appian/simple_vector_store.py): Local RAG using `sentence-transformers`.
- [demo_app.py](file:///C:/Users/gsjit/appian/demo_app.py): Streamlit database dashboard.

**How to Run:**
1.  Install dependencies: `pip install streamlit sentence-transformers faiss-cpu`
2.  Run the app: `python -m streamlit run demo_app.py`
3.  Open the URL (usually `http://localhost:8501`) to interact with the "Appian Knowledge Assistant".

### Verification Recording (v2)
I have recorded a new session to verify system stability and the new UI components.

![Demo Regression Test](file:///C:/Users/gsjit/.gemini/antigravity/brain/50b619c6-e1fa-4838-87cd-8f2160416e75/demo_verification_v2_1766670215752.webp)

**Key Interaction Point: Proactive Context Update**
![Context Update](file:///C:/Users/gsjit/.gemini/antigravity/brain/50b619c6-e1fa-4838-87cd-8f2160416e75/.system_generated/click_feedback/click_feedback_1766670336444.png)
*The retrieval logic works correctly ("Home Policy" found), and the new "Knowledge Base" sidebar is visible on the left.*




## Next Steps
1.  **Deploy Vector DB**: Set up a real instance of Pinecone or Weaviate.

2.  **Configure Appian**: Create the basic objects in Appian Designer using the provided markdown designs.
3.  **End-to-End Test**: Ingest real PDFs and test the retrieval from the Appian Interface.
