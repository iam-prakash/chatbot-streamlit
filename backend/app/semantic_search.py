"""
Semantic search functionality using sentence transformers
"""

from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Dict, Tuple
from .db import get_db_connection, DB_PATH

# Global model instance (load once, reuse)
_model = None

def get_model():
    """Get or create the sentence transformer model"""
    global _model
    if _model is None:
        print("🤖 Loading sentence transformer model...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded successfully")
    return _model

def prepare_documents(db_path: str = DB_PATH) -> List[Tuple[str, str, str, str, str]]:
    """
    Prepare documents from database for semantic search.
    Returns: List of (country, vehicle_type, section, content, full_text) tuples
    """
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM rental_terms")
    rows = c.fetchall()
    conn.close()
    
    documents = []
    sections = ['rental_information', 'payment_information', 'protection_conditions',
                'authorized_driving_areas', 'extras', 'other_charges_and_taxes', 'vat']
    
    for row in rows:
        row_dict = dict(row)
        country = row_dict.get('country', 'Unknown')
        vehicle_type = row_dict.get('vehicle_type', 'Unknown')
        
        # Create a full text document for each row
        full_text_parts = [f"Country: {country}", f"Vehicle Type: {vehicle_type}"]
        
        for section in sections:
            content = row_dict.get(section, '')
            if content and content.strip():
                full_text_parts.append(f"{section.replace('_', ' ').title()}: {content}")
        
        full_text = " ".join(full_text_parts)
        
        # Add individual sections as separate documents for more granular search
        for section in sections:
            content = row_dict.get(section, '')
            if content and content.strip():
                documents.append((
                    country,
                    vehicle_type,
                    section,
                    content,
                    full_text
                ))
    
    return documents

def semantic_search(query: str, db_path: str = DB_PATH, top_k: int = 3) -> List[Dict]:
    """
    Perform semantic search on rental terms database.
    
    Args:
        query: User's question
        db_path: Path to database
        top_k: Number of top results to return
    
    Returns:
        List of dictionaries with search results
    """
    try:
        # Get model and documents
        model = get_model()
        documents = prepare_documents(db_path)
        
        if not documents:
            return []
        
        # Prepare texts for encoding
        doc_texts = [doc[4] for doc in documents]  # Use full_text for better context
        
        # Encode query and documents
        query_embedding = model.encode(query, convert_to_tensor=True)
        doc_embeddings = model.encode(doc_texts, convert_to_tensor=True)
        
        # Compute similarities
        similarities = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]
        
        # Get top-k results
        top_results = torch.topk(similarities, min(top_k, len(similarities)))
        
        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            country, vehicle_type, section, content, full_text = documents[idx]
            results.append({
                'country': country,
                'vehicle_type': vehicle_type,
                'section': section,
                'content': content,
                'full_text': full_text,
                'similarity_score': float(score)
            })
        
        return results
        
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return []

def get_relevant_terms_semantic(query: str, db_path: str = DB_PATH) -> List[Dict]:
    """
    Get relevant rental terms using semantic search.
    Returns individual sections ranked by relevance.
    """
    results = semantic_search(query, db_path, top_k=5)  # Get more results for better coverage
    
    # Return results directly without grouping
    return results 