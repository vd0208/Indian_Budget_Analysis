import streamlit as st
import matplotlib.pyplot as plt
from src.pdf_loader import load_pdfs
from src.chunker import chunk_text
from src.embeddings import create_faiss_index, save_index
from src.retriever import retrieve
from src.analysis import extract_industry_mentions
from src.chatbot import answer_question

st.set_page_config(page_title="Indian Budget Analysis", layout="wide")

st.title(" Indian Budget Industry Analysis (2024–2026)")

# Load PDFs
docs = load_pdfs()

# Chunking
chunks = []
for d in docs:
    chunks.extend(chunk_text(d["text"]))

# Embeddings
index, _ = create_faiss_index(chunks)
save_index(index)

# Analysis
df = extract_industry_mentions(docs)




st.subheader("Sectoral Growth (2024–2026)")

# Create the pivot table using "Sector"
pivot = df.pivot_table(index="Year", columns="Sector", values="Mentions", aggfunc="sum")

# Display the table
st.dataframe(pivot, use_container_width=True)

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
pivot.plot(kind='bar', ax=ax) # Bar charts are better for comparing sector growth
ax.set_ylabel("Number of Mentions")
ax.set_title("Budget Focus Areas by Year")
plt.xticks(rotation=45)
st.pyplot(fig)

# Chatbot
st.subheader("Budget Q&A Chatbot ")

query = st.text_input("Ask a question from the budget documents")

if query:
    retrieved_chunks = retrieve(query, index, chunks)
    context = " ".join(retrieved_chunks)
    answer = answer_question(context, query)
    st.write(answer)
