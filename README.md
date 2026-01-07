AI Structured Data Extraction of Healthcare Records
This project uses Retrieval-Augmented Generation (RAG) and the Gemini 2.5 Flash API to extract structured clinical data from unstructured patient text files. It is designed to maintain strict data isolation between patients while providing a validated, exportable CSV report.

🚀 Features
RAG-Based Retrieval: Uses ChromaDB to index and retrieve relevant medical evidence from patient folders.

Strict Identity Isolation: Automatically creates and destroys temporary vector collections for each patient to prevent data leakage.

Schema Validation: Enforces a strict JSON structure (Name, Diagnosis, Vitals, Medications, Follow-up Plan).

Automated Cleanup: Processes data through a temporary SQLite database and cleans up all temporary files after generating the final report.

Professional Reporting: Generates both a clean CLI table and a patient_report_final.csv file.

🛠️ Setup & Installation
Clone the repository:

Bash

git clone <your-repo-url>
cd AI-structured-data-extraction-of-healthcare-records
Install dependencies:

Bash

pip install pandas chromadb google-genai tabulate
Configure API Key: Replace the API_KEY variable in main.py with your valid Google Gemini API key.

📂 Data Structure
Place your unstructured text files in the data/ directory, organized by patient folders:

Plaintext

data/
├── Patient_1/
│   ├── visit_notes.txt
│   └── lab_results.txt
└── Patient_2/
    └── record.txt
📈 Usage
Run the main extraction script to process the records and generate the report:

Bash

python main.py
The script will output a summary table to your terminal and save the full data to patient_report_final.csv.
