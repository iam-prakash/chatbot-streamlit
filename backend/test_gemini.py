#!/usr/bin/env python3
"""
Test script for Google Gemini integration
"""

import os
import google.generativeai as genai

def test_gemini_connection():
    """Test if Gemini API is working"""
    try:
        # Configure Gemini
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY environment variable not set!")
            print("Please set it with: export GOOGLE_API_KEY='your-api-key'")
            return False
        
        genai.configure(api_key=api_key)  # type: ignore
        
        # Create the model
        model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
        
        # Simple test prompt
        prompt = "Hello! Can you tell me what 2+2 equals?"
        
        print("🤖 Testing Gemini connection...")
        response = model.generate_content(prompt)
        
        print(f"✅ Gemini is working!")
        print(f"Question: {prompt}")
        print(f"Answer: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        return False

def test_qa_without_database():
    """Test Q&A functionality with mock data"""
    try:
        # Configure Gemini
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY not set!")
            return False
        
        genai.configure(api_key=api_key)  # type: ignore
        model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
        
        # Mock rental terms data
        mock_context = """
Rental Terms Entry 1:
Country: USA
Vehicle Type: Passenger vehicle
Rental Information: The minimum age to rent a car is 21 years old. Drivers must have a valid driver's license for at least 1 year.
Payment Information: Credit cards are accepted. A security deposit may be required.
Protection Conditions: Basic insurance is included. Additional coverage options are available.
"""
        
        question = "What is the minimum age to rent a car in the USA?"
        
        prompt = f"""
You are a helpful assistant for Sixt car rental. Answer the customer's question based on the provided rental terms information.

Rental Terms Information:
{mock_context}

Customer Question: {question}

Instructions:
1. Answer the question based ONLY on the provided rental terms information
2. If the information is not available in the provided context, say "I don't have specific information about that in the current rental terms. Please contact Sixt customer service for the most up-to-date information."
3. Be helpful, clear, and concise
4. If the question is about a specific country or vehicle type, mention that in your answer
5. Format your answer in a user-friendly way

Answer:"""
        
        print("🤖 Testing Q&A with mock data...")
        response = model.generate_content(prompt)
        
        print(f"✅ Q&A test successful!")
        print(f"Question: {question}")
        print(f"Answer: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Q&A: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Google Gemini Integration")
    print("=" * 40)
    
    # Test 1: Basic connection
    if test_gemini_connection():
        print("\n" + "=" * 40)
        # Test 2: Q&A functionality
        test_qa_without_database()
    
    print("\n" + "=" * 40)
    print("🎯 Next steps:")
    print("1. Get your API key from: https://makersuite.google.com/app/apikey")
    print("2. Set it with: export GOOGLE_API_KEY='your-api-key'")
    print("3. Run this test again to verify everything works")
    print("4. Fix the scraper to get real data, then test the full system") 