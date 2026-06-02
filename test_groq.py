# test_groq.py
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{
        "role": "user",
        "content": """Rate sentiment of this Hinglish text from -3 to +3.
Text: "yaar ye phone ekdum mast hai, totally worth it"
Return ONLY JSON: {"score": 2.5, "confidence": "high"}"""
    }],
    max_tokens=50
)
print(response.choices[0].message.content)