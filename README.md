Indian Budget Analysis AI (2024–2026)

An end-to-end **RAG (Retrieval-Augmented Generation)** application designed to analyze the Indian Union Budgets from 2024 to 2026. This tool combines deterministic keyword analysis for sectoral growth visualization with a local LLM (Ollama) for intelligent Q&A.

##  Features
- **Semantic Search (RAG):** Ask complex questions about budget allocations and get answers grounded in official PDF data.
- **Sectoral Growth Tracking:** Visualizes industry mentions (Tech, Agriculture, Infrastructure, etc.) across multiple years using Matplotlib.
- **Privacy-First:** Processes all data locally using **FAISS** for vector storage and **Ollama (Llama 3)** for generation.
- **Interactive UI:** A clean, multi-functional dashboard built with Streamlit.

##  Tech Stack
- **LLM:** Ollama (Llama 3)
- **Vector Database:** FAISS
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Frontend:** Streamlit
- **PDF Processing:** PyMuPDF (Fitz)
- **Data Analysis:** Pandas & Matplotlib

## Credits & Acknowledgments
- **Developer:** Vian Dsouza
- **AI used:** I used **Gemini**(free version) to help mw in debugging, optimizing the FAISS retrieval logic, and refining the sectoral analysis methodology.
- **Data Source:** Official Union Budget Documents, Government of India (2024–2026).

## Installation

1. Clone the repository:
  
   git clone [https://github.com/your-username/indian-budget-analysis-ai.git](https://github.com/your-username/indian-budget-analysis-ai.git)
   cd indian-budget-analysis-ai

2. Install dependencies:

pip install -r requirements.txt

3. Install & Run Ollama: Download from ollama.com and pull the model:

ollama pull llama3

4. Add your Data: Place your budget PDFs in the /data folder.
name it as budget_2024, budget_2025, budget_2026

5. Run the App:

streamlit run app.py


**How it Works**
Extraction: Chunks text from PDFs and generates embeddings.

Indexing: Stores vectors in a FAISS index for high-speed retrieval.

Analysis: Scans for specific industry keywords to plot year-over-year trends.

Q&A: When a user asks a question, the system retrieves relevant context and passes it to Ollama to generate a factual response.