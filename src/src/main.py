import os
import sqlite3
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Load API Key
load_dotenv()

# --- 1. Define Structured Output Schema ---
class PatientSummary(BaseModel):
    diagnosis: str = Field(description="The primary medical condition")
    avg_blood_pressure: str = Field(description="The average BP reading")
    medications: list = Field(description="List of all medications found")

# --- 2. Database Logic ---
def save_to_db(patient_id, data):
    conn = sqlite3.connect('healthcare_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            diagnosis TEXT,
            vitals TEXT,
            medications TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        INSERT INTO summaries (patient_id, diagnosis, vitals, medications)
        VALUES (?, ?, ?, ?)
    ''', (patient_id, data['diagnosis'], data['avg_blood_pressure'], str(data['medications'])))
    conn.commit()
    conn.close()

# --- 3. Main AI Extraction Logic ---
def run_structured_extraction(patient_folder):
    path = f"./data/{patient_folder}/"
    loader = DirectoryLoader(path, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    parser = JsonOutputParser(pydantic_object=PatientSummary)
    prompt = ChatPromptTemplate.from_template(
        "Extract medical info from context: {context}\n{format_instructions}",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    
    # Retrieve relevant snippets
    context_docs = vectorstore.similarity_search("vitals and diagnosis", k=5)
    context_text = "\n".join([d.page_content for d in context_docs])
    
    chain = prompt | llm | parser
    return chain.invoke({"context": context_text})

# --- 4. Batch Processor ---
def process_all_patients():
    data_dir = './data'
    # List all patient folders
    patient_folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    
    for folder in patient_folders:
        print(f"🔄 Processing {folder}...")
        try:
            result = run_structured_extraction(folder)
            save_to_db(folder, result)
            print(f"✅ Success: {folder} saved to database.")
        except Exception as e:
            print(f"❌ Error with {folder}: {e}")

if __name__ == "__main__":
    process_all_patients()