import gradio as gr
import google.generativeai as genai

import os

MODEL = "gemini-2.5-flash"

API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

def generate_report(text):
    prompt = f"""
Extract patient information using EXACTLY this format:

Patient Name: ...
Diagnosis: ...
Vitals: ...
Medications: ...
Follow Up Plan: ...

No extra text.

Clinical notes:
{text}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()

interface = gr.Interface(
    fn=generate_report,
    inputs=gr.Textbox(lines=15, label="Paste Clinical Notes"),
    outputs="text",
    title="AI Structured Healthcare Data Extraction"
)

interface.launch()
