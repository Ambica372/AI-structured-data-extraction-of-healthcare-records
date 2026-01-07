# 🏥 Healthcare AI: Structured Data Extraction (RAG)

## Project Architecture


1. **Data Ingestion**: Synthetic records generated via `faker`.
2. **Vectorization**: Records embedded using `GoogleGenerativeAIEmbeddings` and stored in `ChromaDB`.
3. **Extraction**: `Gemini-1.5-Flash` performs RAG-based extraction with `Pydantic` validation.
4. **Persistence**: Structured results are saved to a local `SQLite` database for clinical review.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Generate the dataset: `python src/generate_dataset.py`
3. Run the AI pipeline: `python src/main.py`