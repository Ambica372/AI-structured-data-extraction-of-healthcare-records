import json
import sqlite3
import pathlib
import time
from google import genai
from google.genai import types

# --- 1. CONFIGURATION ---
API_KEY = "AIzaSyDatDvj9ZPKwMUVZnCIFO0dorxGiI53oB8"
MODEL_ID = "gemini-2.5-flash" 

def run_batch_extraction():
    print(f"📡 Initializing Resilient Batch Extraction...")
    
    client = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(api_version='v1')
    )

    root_data = pathlib.Path("data")
    patient_folders = [f for f in root_data.iterdir() if f.is_dir()]

    conn = sqlite3.connect("healthcare_2026.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS records (patient_id TEXT, diagnosis TEXT, data TEXT)")

    for folder in patient_folders:
        print(f"\n📂 Processing {folder.name}...")
        
        combined_notes = ""
        for file in folder.glob("*.txt"):
            with open(file, "r") as f:
                combined_notes += f.read() + "\n"

        if not combined_notes:
            continue

        # --- RETRY LOGIC FOR 503 ERRORS ---
        success = False
        attempts = 0
        max_retries = 3
        
        while not success and attempts < max_retries:
            try:
                prompt = f"Extract to a SINGLE JSON object: patient_name, diagnosis, vitals, meds. Text: {combined_notes}"
                response = client.models.generate_content(model=MODEL_ID, contents=prompt)
                
                raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
                extracted = json.loads(raw_text)
                data = extracted[0] if isinstance(extracted, list) else extracted

                cursor.execute("INSERT INTO records VALUES (?, ?, ?)", 
                               (folder.name, data.get('diagnosis', 'Unknown'), json.dumps(data)))
                conn.commit()
                print(f"✅ Saved results for {data.get('patient_name', folder.name)}")
                success = True

            except Exception as e:
                if "503" in str(e) or "overloaded" in str(e).lower():
                    attempts += 1
                    wait_time = attempts * 5  # Wait 5, 10, 15 seconds
                    print(f"⚠️ Server busy (503). Retrying in {wait_time}s... (Attempt {attempts}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Permanent error for {folder.name}: {e}")
                    break # Don't retry for non-server errors (like code bugs)

    conn.close()
    print("\n🏁 BATCH PROCESSING COMPLETE!")

if __name__ == "__main__":
    run_batch_extraction()