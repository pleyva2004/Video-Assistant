def context_prompt(question, chunks):

    context = ""
    for chunk in chunks:
        context += f"Chunk {chunk['chunk_index']}: {chunk['text']}\n\n"

    prompt = f"""Answer the following question using the transcript context below:

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    return prompt

def context_prompt_history(question, chunks, history):

    context = ""
    for chunk in chunks:
        context += f"Chunk {chunk['chunk_index']}: {chunk['text']}\n\n"

    for query, answer in history[-5:]:
        context += f"Question: {query}\nAnswer: {answer}\n\n"

    prompt = f"""Answer the following question using the transcript context below and the history of the conversation:

    Context:
    {context}

    History:
    {history}

    Question:
    {question}


    Answer:
    """

    return prompt