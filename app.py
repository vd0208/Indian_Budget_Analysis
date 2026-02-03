import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import re
from src.pdf_loader import load_pdfs
from src.chunker import chunk_text
from src.embeddings import create_faiss_index, save_index
from src.retriever import retrieve
from src.analysis import extract_industry_mentions
from src.chatbot import answer_question

# --- Page Setup ---
st.set_page_config(page_title="Indian Budget Analysis", layout="wide")

# --- Sidebar ---
st.sidebar.title(" Analysis Controls")
available_years = ["2024", "2025", "2026"]
selected_years = st.sidebar.multiselect(
    "Select Budget Years to Analyze:",
    options=available_years,
    default=available_years
)



st.title("Indian Budget Industry Analysis (2024–2026)")

# --- Data Engine (Cached) ---
@st.cache_resource
def get_system_data():
    docs = load_pdfs()
    all_chunks = []
    # We tag each chunk with its source so we can filter it later
    for d in docs:
        year_match = re.search(r"\d{4}", d["source"])
        doc_year = year_match.group(0) if year_match else "Unknown"
        for c in chunk_text(d["text"]):
            all_chunks.append(f"[{doc_year}] {c}")
    
    index, _ = create_faiss_index(all_chunks)
    raw_df = extract_industry_mentions(docs)
    return all_chunks, index, raw_df

chunks, index, df = get_system_data()

# --- 1. Dynamic Visualization Section ---
st.subheader(f"Sectoral Growth Trends ({', '.join(selected_years) if selected_years else 'None'})")

if selected_years:
    # Filter DF for charts
    filtered_df = df[df['Year'].isin(selected_years)]
    pivot = filtered_df.pivot_table(index="Sector", columns="Year", values="Mentions", aggfunc="sum")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(pivot, use_container_width=True)
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        pivot.plot(kind='bar', ax=ax)
        ax.set_ylabel("Keyword Mentions")
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.warning("Please select at least one year in the sidebar.")

# --- 2. Chatbot Section with Metadata Filtering ---
st.divider()
st.subheader("Budget Q&A Chatbot")

query = st.text_input("Ask a question about the selected budget years:")

if query:
    if not selected_years:
        st.error("Select a year in the sidebar to provide context to the AI.")
    else:
        # Retrieve potential matches
        raw_retrieved = retrieve(query, index, chunks)
        
        # FILTER: Only keep chunks that start with the selected year tags
        # Example: Keeps "[2026] text..." if 2026 is selected.
        context_chunks = [
            c for c in raw_retrieved 
            if any(f"[{y}]" in c for y in selected_years)
        ]

        if not context_chunks:
            st.warning("No relevant information found for the selected years.")
        else:
            context = " ".join(context_chunks)
            with st.spinner(f"Searching {selected_years} documents..."):
                answer = answer_question(context, query)
                st.write("### Answer")
                st.info(answer)
                
                with st.expander("View Source Context (just for refernce)"):
                    st.write(context_chunks)