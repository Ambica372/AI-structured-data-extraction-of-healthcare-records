import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

# 1. Load Environment Variables (API Key)
load_dotenv()

def run_healthcare_extraction(patient_id, patient_name):
    print(f"\n🚀 Analyzing records for {patient_name} ({patient_id})...")
    
    # 2. Load the 10 files from the data folder
    path = f"./data/{patient_id}/"
    loader = DirectoryLoader(path, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()

    # 3. Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    # 4. Create Vector Database (In-Memory for now)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    # 5. Define the Medical Prompt
    template = """
    You are a professional Medical Registrar. Summarize the following clinical notes 
    into a structured format including:
    - Primary Symptoms/Observations
    - Recorded Vitals (Average BP/HR)
    - Recommended Follow-up
    
    Context: {context}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # 6. Retrieve info and generate response
    context_docs = vectorstore.similarity_search("vitals and diagnosis", k=5)
    context_text = "\n".join([d.page_content for d in context_docs])
    
    chain = prompt | llm
    response = chain.invoke({"context": context_text})
    
    print(f"--- MEDICAL SUMMARY: {patient_name} ---")
    print(response.content)

if __name__ == "__main__":
    # Test for Patient 1
    run_healthcare_extraction("Patient_1", "Arjun Kumar")