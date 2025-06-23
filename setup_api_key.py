#!/usr/bin/env python3
"""
Google API Key Setup Helper
This will help you set your Google API key and test AI functionality.
"""

import os

def main():
    print("🔑 GOOGLE API KEY SETUP")
    print("=" * 50)
    
    # Check current status
    current_key = os.environ.get('GOOGLE_API_KEY')
    if current_key:
        print(f"✅ API key is already set (length: {len(current_key)})")
        choice = input("🤔 Do you want to update it? (y/n): ").lower()
        if choice != 'y':
            print("✅ Keeping current API key")
            return current_key
    
    print("\n📋 To get your Google API key:")
    print("1. Go to: https://aistudio.google.com/")
    print("2. Sign in with your Google account")
    print("3. Click 'Get API key' button")
    print("4. Create a new API key")
    print("5. Copy the key")
    
    print("\n🔧 Enter your Google API key:")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key entered")
        return None
    
    if len(api_key) < 20:
        print("⚠️  API key seems too short. Google API keys are usually longer.")
        confirm = input("Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            return None
    
    # Set the environment variable for this session
    os.environ['GOOGLE_API_KEY'] = api_key
    print(f"✅ API key set for this session")
    
    # Show how to set it permanently
    print(f"\n💡 To set permanently in PowerShell, run:")
    print(f'   $env:GOOGLE_API_KEY="{api_key}"')
    print(f"\n💡 To set permanently in Windows, run:")
    print(f'   setx GOOGLE_API_KEY "{api_key}"')
    
    return api_key

if __name__ == "__main__":
    api_key = main()
    
    if api_key:
        print(f"\n🧪 Testing API key...")
        
        # Import and run the test
        try:
            from test_api_key import test_ai_connection
            success = test_ai_connection()
            
            if success:
                print("\n🎉 SUCCESS! Your API key is working!")
                print("🤖 Your agents can now use real Google AI!")
            else:
                print("\n❌ API key test failed")
                
        except ImportError:
            print("⚠️  Test module not found, but API key is set")
    
    print("\n" + "=" * 50) 