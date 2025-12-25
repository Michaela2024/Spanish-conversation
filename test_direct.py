import google.generativeai as genai

# Put your ACTUAL full API key here temporarily for testing
API_KEY = "AIzaSyC-YOUR-FULL-KEY"

print(f"Testing with key: {API_KEY[:15]}...")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello in 5 words")
    print("SUCCESS!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"ERROR: {e}")
