import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
)

SYSTEM_PROMPT = """
You are an intent classification engine.

Return ONLY valid JSON in this schema:
{
  "can_reply": boolean,
  "urgency": "low" | "medium" | "high",
  "reply_text": string | null,
  "confidence": number
}
"""

def classify_message(message, context):
    prompt = f"""
Context:
{context}

Message:
{message}
"""

    response = MODEL.generate_content(
        [SYSTEM_PROMPT, prompt]
    )

    return response.candidates[0].content.parts[0].text
