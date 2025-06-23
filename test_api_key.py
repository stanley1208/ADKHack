#!/usr/bin/env python3
"""Test Google API key configuration and AI capabilities"""

import os

def check_api_key():
    """Check if Google API key is configured"""
    print("🔑 Checking Google API Key Configuration...")
    print("=" * 50)
    
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    if api_key:
        print(f"✅ GOOGLE_API_KEY is set")
        print(f"📏 Length: {len(api_key)} characters")
        print(f"🔍 Preview: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else api_key}")
        return True
    else:
        print("❌ GOOGLE_API_KEY is not set")
        print("💡 Set it with: set GOOGLE_API_KEY=your-api-key")
        return False

def test_ai_connection():
    """Test connection to Google AI services"""
    print("\n🤖 Testing Google AI Connection...")
    print("=" * 50)
    
    try:
        from google.genai import Client
        client = Client()
        print("✅ Google AI client created successfully")
        
        # Test basic AI call
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents="Say 'Hello from Google AI!' if you can hear me."
        )
        
        if response and response.text:
            print(f"✅ AI Response: {response.text}")
            return True
        else:
            print("❌ No response from AI")
            return False
            
    except Exception as e:
        print(f"❌ AI connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 GOOGLE API KEY & AI TESTING")
    
    key_ok = check_api_key()
    
    if key_ok:
        ai_ok = test_ai_connection()
        
        if ai_ok:
            print("\n🎉 SUCCESS: Ready for AI-powered agents!")
        else:
            print("\n⚠️  API key set but AI connection failed")
    else:
        print("\n🔧 Please set your Google API key first")
    
    print("=" * 50) 