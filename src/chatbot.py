import ollama

def answer_question(context, question):
    """
    Uses Ollama to generate an answer based on budget context.
    Using 'llama3' as it's great for reasoning over financial data.
    """
    
    prompt = (
        f"You are a financial analyst. Using only the context provided below from the "
        f"Indian Budget (2024-2026), answer the user's question.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Answer concisely with key figures if available:"
    )

    try:
        response = ollama.generate(
            model='llama3',
            prompt=prompt,
            options={
                'temperature': 0.2, # Keep it factual
                'top_p': 0.9
            }
        )
        return response['response'].strip()
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}. Make sure the Ollama app is running."