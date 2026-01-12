from google import genai
import json
from app.logger import logger
import os

def get_genai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("Google API key is missing! Set it in environment variables.")
        return None  # Return None instead of crashing
    return genai.Client(api_key=api_key)

def summarize_text_and_category(text: str) -> dict:
    client = get_genai_client()
    if client is None:
        return {"summary": "", "category": ""}  # fail gracefully

    prompt_text = f"""
Read the following text and do two things:
1. Summarize it in a short, clear paragraph in simple English.
2. Detect its category freely.

Text:
{text}

Return JSON like this:
{{"summary": "...", "category": "..."}}
"""

    try:
        logger.info("Sending request to Google Gemini model...")
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt_text
        )
        output_text = response.text.strip()
        logger.debug(f"Raw model output: {output_text}")

        # Remove triple backticks if present
        if output_text.startswith("```"):
            output_text = output_text.split("\n", 1)[1]
            output_text = output_text.rsplit("```", 1)[0]

        # Parse JSON
        try:
            parsed = json.loads(output_text)
            summary = parsed.get("summary", "").strip()
            category = parsed.get("category", "").strip()
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON. Returning raw output.")
            summary = output_text
            category = output_text

        return {"summary": summary, "category": category}

    except Exception as e:
        logger.exception(f"Error calling Google AI: {e}")
        return {"summary": "", "category": ""}
