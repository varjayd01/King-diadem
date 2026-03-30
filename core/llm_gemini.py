import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

def ask_gemini(prompt):
    try:
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"LLM ERROR: {str(e)}"
