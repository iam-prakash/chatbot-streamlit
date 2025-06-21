import google.generativeai as genai  # type: ignore
from .db import get_db_connection, DB_PATH
from .semantic_search import get_relevant_terms_semantic
import os
from typing import List, Dict, Optional

# Configure Gemini
# You'll need to set GOOGLE_API_KEY environment variable
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))  # type: ignore

def get_relevant_terms(query: str, db_path: str = DB_PATH) -> List[Dict]:
    """Retrieve relevant rental terms from database using semantic search"""
    return get_relevant_terms_semantic(query, db_path)

def format_context_for_gemini(terms_data: List[Dict]) -> str:
    """Format the retrieved terms data into a context string for Gemini, with most relevant section highlighted."""
    if not terms_data:
        return "No relevant rental terms found."
    
    # Find the most relevant section (highest similarity_score)
    most_relevant = max(terms_data, key=lambda x: x.get('similarity_score', 0))
    
    # Build the targeted context
    context_parts = []
    
    # Add the most relevant section at the top
    if most_relevant.get('section') and most_relevant.get('content'):
        section_name = most_relevant['section'].replace('_', ' ').title()
        context_parts.append(f"Most relevant section:\n{section_name}: {most_relevant['content']}\n")
    else:
        context_parts.append("Most relevant section: Not found\n")
    
    # Add the rest of the context for reference
    context_parts.append("Full rental terms context (for reference):\n")
    
    # Group by country and vehicle type for the full context
    grouped_data = {}
    for result in terms_data:
        key = (result['country'], result['vehicle_type'])
        if key not in grouped_data:
            grouped_data[key] = {
                'country': result['country'],
                'vehicle_type': result['vehicle_type'],
                'sections': {}
            }
        grouped_data[key]['sections'][result['section']] = result['content']
    
    # Format the grouped data
    for i, (key, data) in enumerate(grouped_data.items(), 1):
        context_parts.append(f"Rental Terms Entry {i}:")
        context_parts.append(f"Country: {data['country']}")
        context_parts.append(f"Vehicle Type: {data['vehicle_type']}")
        
        for section_name, content in data['sections'].items():
            if content and content.strip():
                context_parts.append(f"{section_name.replace('_', ' ').title()}: {content}")
        context_parts.append("")
    
    return "\n".join(context_parts)

def generate_answer_with_gemini(question: str, context: str) -> str:
    """Generate an answer using Google Gemini based on the question and context"""
    try:
        # Create the model
        model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
        
        # Create the prompt
        prompt = f"""
You are a helpful assistant for Sixt car rental. Answer the customer's question based on the provided rental terms information.

Rental Terms Information:
{context}

Customer Question: {question}

Instructions:
1. Answer the question based on the provided rental terms information
2. If the information is available in the provided context, provide a clear and helpful answer
3. If the information is not available in the provided context, say "I don't have specific information about that in the current rental terms. Please contact Sixt customer service for the most up-to-date information."
4. Be helpful, clear, and concise
5. If the question is about a specific country or vehicle type, mention that in your answer
6. Format your answer in a user-friendly way
7. Don't be overly cautious - if the information is there, provide it confidently

Answer:"""
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I encountered an error while processing your question. Please try again or contact customer service. Error: {str(e)}"

def answer_question(question: str, db_path: str = DB_PATH) -> Dict:
    """Main function to answer a question using RAG (Retrieval Augmented Generation)"""
    # Step 1: Retrieve relevant terms
    relevant_terms = get_relevant_terms(question, db_path)
    
    # Step 2: Format context
    context = format_context_for_gemini(relevant_terms)
    
    # Debug: Print the context being sent to LLM
    print(f"DEBUG - Context being sent to LLM:")
    print(f"Context length: {len(context)} characters")
    print(f"Context preview: {context[:500]}...")
    print(f"Number of relevant terms: {len(relevant_terms)}")
    if relevant_terms:
        print(f"Top similarity score: {relevant_terms[0].get('similarity_score', 'N/A')}")
    
    # Step 3: Generate answer with Gemini
    answer = generate_answer_with_gemini(question, context)
    
    return {
        "question": question,
        "answer": answer,
        "sources": relevant_terms,  # Include source data for transparency
        "context_used": context[:500] + "..." if len(context) > 500 else context  # Truncated for response
    } 