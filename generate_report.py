!pip install chromadb google-generativeai

import pathlib
import pandas as pd
import chromadb
from google import genai
import os

# ========== CONFIG ==========
API_KEY = "enter_api_key"
MODEL = "gemini-2.5-flash"
DATA_DIR = "/data"
OUTPUT_FILE = "patient_report_final.csv"
# ============================

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError("Folder /data not found")

client = genai.Client(api_key=API_KEY)
chroma = chromadb.Client()

rows = []

# ---------- HELPERS ----------

def safe(value):
    return value if value else "Not mentioned"

def cross_patient_check(text, current_patient):
    text = text.lower()
    for p in ["patient_1", "patient_2", "patient_3"]:
        if p != current_patient.lower() and p in text:
            return False
    return True

def parse_output(text):
    result = {
        "patient_name": "Not mentioned",
        "diagnosis": "Not mentioned",
        "vitals": "Not mentioned",
        "medications": "Not mentioned",
        "follow_up_plan": "Not mentioned"
    }

    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.lower().strip()
        value = value.strip()

        if "patient name" in key:
            result["patient_name"] = value
        elif "diagnosis" in key:
            result["diagnosis"] = value
        elif "vitals" in key:
            result["vitals"] = value
        elif "medications" in key:
            result["medications"] = value
        elif "follow up" in key:
            result["follow_up_plan"] = value

    return result

# ---------- MAIN LOOP ----------

for patient_dir in pathlib.Path(DATA_DIR).iterdir():
    if not patient_dir.is_dir():
        continue

    print(f"Processing {patient_dir.name}")

    collection = chroma.get_or_create_collection(patient_dir.name)

    for file in patient_dir.glob("*.txt"):
        collection.add(documents=[file.read_text()], ids=[file.name])

    docs = collection.query(
        query_texts=["extract patient medical details"],
        n_results=3
    )["documents"][0]

    context = "\n".join(docs)

    prompt = f"""
Extract patient information using EXACTLY this format:

Patient Name: ...
Diagnosis: ...
Vitals: ...
Medications: ...
Follow Up Plan: ...

No extra text.

Clinical notes:
{context}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    raw = response.text.strip()

    if not cross_patient_check(raw, patient_dir.name):
        print("❌ Cross-patient contamination detected")
        chroma.delete_collection(patient_dir.name)
        continue

    parsed = parse_output(raw)

    rows.append({
        "id": patient_dir.name,
        **parsed
    })

    chroma.delete_collection(patient_dir.name)

# ---------- SAVE ----------

df = pd.DataFrame(rows)

# Make display readable in Colab
pd.set_option("display.max_colwidth", 80)

df.to_csv(OUTPUT_FILE, index=False)

print(f"\n✅ CSV generated cleanly: {OUTPUT_FILE}")
display(df)
