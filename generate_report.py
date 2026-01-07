import json
import sqlite3
import pathlib
import os
import pandas as pd
import chromadb
from google import genai
from google.genai import types
from tabulate import tabulate

# --- CONFIGURATION ---
API_KEY = "AIzaSyDatDvj9ZPKwMUVZnCIFO0dorxGiI53oB8"
MODEL_ID = "gemini-2.5-flash"
DB_NAME = "temp_healthcare.db"

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "patient_name": {"type": "STRING"},
        "diagnosis": {"type": "STRING"},
        "vitals": {"type": "ARRAY", "items": {"type": "STRING"}},
        "medications": {"type": "ARRAY", "items": {"type": "STRING"}},
        "follow_up_plan": {"type": "STRING"}
    },
    "required": ["patient_name", "diagnosis", "vitals", "medications", "follow_up_plan"]
}

def run_final_system():
    client = genai.Client(api_key=API_KEY)
    chroma_client = chromadb.Client()
    
    # Setup temporary storage
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS records (id TEXT, data TEXT)")

    patient_folders = [f for f in pathlib.Path("data").iterdir() if f.is_dir()]

    for folder in patient_folders:
        print(f"🔄 Processing {folder.name}...")
        
        # RAG Indexing
        coll_name = f"c_{folder.name.lower().replace('_', '')}"
        collection = chroma_client.get_or_create_collection(name=coll_name)
        for file in folder.glob("*.txt"):
            collection.add(documents=[file.read_text()], ids=[file.name])

        # Retrieval
        results = collection.query(query_texts=["medical details"], n_results=3)
        context = "\n".join(results['documents'][0])
        if len(context.strip()) < 50:
            context = "\n".join([f.read_text() for f in folder.glob("*.txt")])

        # AI Extraction
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=f"Extract JSON from:\n{context}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RESPONSE_SCHEMA
                )
            )
            cursor.execute("INSERT INTO records VALUES (?, ?)", (folder.name, response.text))
            conn.commit()
        except Exception as e:
            print(f"⚠️ Error on {folder.name}: {e}")
        
        chroma_client.delete_collection(name=coll_name)

    # Export and Cleanup
    df = pd.read_sql_query("SELECT * FROM records", conn)
    conn.close()

    if not df.empty:
        # Format the final report
        final_data = [json.loads(r) for r in df['data']]
        report_df = pd.concat([df[['id']], pd.DataFrame(final_data)], axis=1)
        report_df.to_csv("patient_report_final.csv", index=False)
        
        # Print Table
        print("\n" + "═"*50)
        print(tabulate(report_df[['id', 'patient_name', 'diagnosis']], headers='keys', tablefmt='psql'))
        print("═"*50)
        print("✅ Success! CSV generated and temporary database deleted.")
    
    # Remove the .db file to keep the folder clean
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

if __name__ == "__main__":
    run_final_system()