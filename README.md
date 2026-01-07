# AI Structured Data Extraction of Healthcare Records

## Overview
This project presents a robust AI-based system for extracting **structured clinical information** from **unstructured healthcare text records** using **Retrieval-Augmented Generation (RAG)** and the **Gemini 2.5 Flash API**.  

The pipeline is designed to ensure **strict patient-level data isolation**, **schema validation**, and **secure processing**, producing a reliable and exportable CSV report suitable for healthcare analytics and downstream AI systems.

---

## Project Objectives
- Convert unstructured medical text into structured clinical data
- Ensure complete isolation between patient records
- Enforce strict schema validation for reliable outputs
- Generate professional, reusable CSV reports

---

## Key Features

### Retrieval-Augmented Generation (RAG)
- Uses **ChromaDB** to index and retrieve relevant medical context.
- Grounds LLM responses on patient-specific documents for accurate extraction.

### Strict Patient Identity Isolation
- Creates **temporary vector collections per patient**.
- Automatically destroys collections after processing to prevent data leakage.

### Schema-Enforced Extraction
The extracted data strictly follows this schema:
- Name  
- Diagnosis  
- Vitals  
- Medications  
- Follow-up Plan  

All outputs are validated before inclusion in the final report.

### Automated Cleanup
- Uses a **temporary SQLite database** for intermediate storage.
- Cleans up vector stores and temporary files after execution.

### Professional Reporting   

- Displays a clean, formatted summary table in the CLI.
- Generates a validated CSV file:


---

## Technology Stack
- Python  
- Pandas  
- ChromaDB  
- Google Gemini 2.5 Flash API  
- SQLite  
- Tabulate  

---

## Repository Structure
AI-structured-data-extraction-of-healthcare-records/
├── main.py
├── data/
│ ├── Patient_1/
│ │ ├── visit_notes.txt
│ │ └── lab_results.txt
│ └── Patient_2/
│ └── record.txt
├── patient_report_final.csv
├── requirements.txt
└── README.md


---

## Setup and Installation

### Clone the Repository
git clone <your-repo-url>
cd AI-structured-data-extraction-of-healthcare-records


### Install Dependencies
pip install pandas chromadb google-genai tabulate


### API Configuration
Open `main.py` and replace the `API_KEY` variable with your valid **Google Gemini API key**.

---

## Data Organization
Place unstructured healthcare text files inside the `data/` directory, organized by patient folders.

data/
├── Patient_1/
│ ├── visit_notes.txt
│ └── lab_results.txt
└── Patient_2/
└── record.txt

Each patient folder is processed independently to guarantee data isolation.

---

## Usage
Run the extraction pipeline:

python main.py


### Output
- Structured summary table printed in the terminal
- Final validated CSV saved as:
patient_report_final.csv


---

## Use Cases
- Healthcare data preprocessing
- Clinical documentation structuring
- Medical analytics pipelines
- Secure AI-driven healthcare data extraction
- Research and academic applications

---

## Project Status
Completed and functional.  
Designed for extensibility to support additional schemas, medical domains, and integration with downstream healthcare systems.

---

## Author
Ambica Natraj
