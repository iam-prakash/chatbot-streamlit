#!/usr/bin/env python3
"""
Test script to debug the QA system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.qa import answer_question

def test_qa_debug():
    """Test the QA system with debug output"""
    
    test_questions = [
        "Can I drive the rental car to Canada?",
        "What is the minimum age to rent a car in the USA?",
        "What payment methods are accepted?"
    ]
    
    print("🧪 Testing QA System with Debug Output")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\n🔍 Question: {question}")
        print("-" * 30)
        
        try:
            result = answer_question(question)
            print(f"✅ Answer: {result['answer']}")
            print(f"📊 Sources count: {len(result['sources'])}")
            if result['sources']:
                print(f"🎯 Top similarity score: {result['sources'][0].get('similarity_score', 'N/A')}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Debug test completed!")

if __name__ == "__main__":
    test_qa_debug() 