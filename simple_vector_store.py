import os
import uuid
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class LocalKnowledgeBase:
    def __init__(self):
        print("Loading embedding model (all-MiniLM-L6-v2)...")
        # Lightweight model for local use
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks = []
        self.embeddings = None
        print("Model loaded.")

    def add_document(self, text: str, metadata: Dict):
        """
        Splits text into chunks and stores them with metadata.
        """
        # Simple chunking for demo
        chunk_size = 300
        overlap = 50
        
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end]
            
            chunk_data = {
                "id": str(uuid.uuid4()),
                "text": chunk_text,
                "metadata": metadata
            }
            self.chunks.append(chunk_data)
            start += (chunk_size - overlap)
            
        print(f"Added document. Total chunks: {len(self.chunks)}")

    def build_index(self):
        """
        Generates embeddings for all chunks.
        """
        if not self.chunks:
            return
            
        texts = [c["text"] for c in self.chunks]
        print(f"Generating embeddings for {len(texts)} chunks...")
        self.embeddings = self.model.encode(texts)
        print("Index built.")

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Performs vector search using cosine similarity.
        """
        if self.embeddings is None:
            return []
            
        query_embedding = self.model.encode([query])[0]
        
        # Calculate Cosine Similarity
        # (A . B) / (|A| * |B|)
        # Since SentenceTransformer embeddings are normalized, just dot product works often, 
        # but let's be explicit.
        scores = np.dot(self.embeddings, query_embedding)
        
        # Get top K indices
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "chunk": self.chunks[idx],
                "score": float(scores[idx])
            })
            
        return results

# Dummy Data Loader
def load_dummy_data(kb: LocalKnowledgeBase):
    # Doc 1: Auto Policy
    kb.add_document(
        text="""
        AUTOMOBILE CLAIM POLICY v2024
        
        Section 1: Coverage
        We cover accidental damage to your vehicle. 
        For flood damage, coverage applies only if Comprehensive Insurance was purchased.
        
        Section 2: Claims Process in Florida
        In Florida, you must file a police report within 24 hours for any accident exceeding $500.
        The statute of limitations for filing a claim is 4 years.
        
        Section 3: Exclusions
        Wear and tear, rust, and mechanical breakdown are not covered.
        Damage caused by intentional acts is excluded.
        """,
        metadata={"doc_name": "Auto Policy 2024", "page": 12, "url": "http://docs/auto_policy_2024.pdf"}
    )
    
    # Doc 2: Homeowners Policy
    kb.add_document(
        text="""
        HOMEOWNERS INSURANCE GUIDELINES
        
        Flood coverage is EXCLUDED from standard policies. 
        You must purchase a separate FEMA flood policy.
        
        In case of fire, evacuate immediately and call 911. 
        Report the loss within 72 hours.
        """,
        metadata={"doc_name": "Home Policy 2024", "page": 5, "url": "http://docs/home_policy.pdf"}
    )
    
    kb.build_index()
