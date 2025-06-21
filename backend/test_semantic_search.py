#!/usr/bin/env python3
"""
Test script for semantic search functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.semantic_search import get_relevant_terms_semantic, semantic_search

def test_semantic_search():
    """Test semantic search with various queries"""
    
    test_queries = [
        "What is the minimum age to rent a car in the USA?",
        "How much does it cost to rent a car in Germany?",
        "What insurance is included with the rental?",
        "Can I drive the car to another country?",
        "What payment methods are accepted?",
        "What happens if I return the car late?",
        "Do I need a credit card to rent?",
        "What documents do I need to rent a car?"
    ]
    
    print("🧪 Testing Semantic Search")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 30)
        
        # Test semantic search
        results = get_relevant_terms_semantic(query)
        
        if results:
            for i, result in enumerate(results[:2], 1):  # Show top 2 results
                print(f"Result {i}:")
                print(f"  Country: {result['country']}")
                print(f"  Vehicle Type: {result['vehicle_type']}")
                print(f"  Similarity Score: {result.get('similarity_score', 'N/A'):.3f}")
                
                # Show which sections have content
                sections_with_content = []
                for section in ['rental_information', 'payment_information', 'protection_conditions',
                               'authorized_driving_areas', 'extras', 'other_charges_and_taxes', 'vat']:
                    if result.get(section, '').strip():
                        sections_with_content.append(section.replace('_', ' ').title())
                
                print(f"  Relevant Sections: {', '.join(sections_with_content)}")
                print()
        else:
            print("  No results found")
    
    print("=" * 50)
    print("✅ Semantic search test completed!")

if __name__ == "__main__":
    test_semantic_search() 