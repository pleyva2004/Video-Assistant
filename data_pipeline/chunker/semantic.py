from sentence_transformers import SentenceTransformer
from transformers import GPT2TokenizerFast
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download('punkt_tab')

def semantic_chunks_embeddings(text, sim_threshold=0.7, min_chunk_sentences=4):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = nltk.sent_tokenize(text)
    sentence_embeddings = model.encode(sentences, show_progress_bar=True, convert_to_numpy=True)

    chunks = []
    current_chunk = [sentences[0]]
    current_chunk_embeddings = [sentence_embeddings[0]]

    for i in range(1, len(sentences)):
        sim = cosine_similarity([sentence_embeddings[i-1]], [sentence_embeddings[i]])[0][0]
        current_chunk.append(sentences[i])
        current_chunk_embeddings.append(sentence_embeddings[i])

        # Boundary detection
        if sim < sim_threshold and len(current_chunk) >= min_chunk_sentences:
            chunk_text = " ".join(current_chunk)
            chunk_embedding = model.encode(chunk_text)
            chunks.append((chunk_text, chunk_embedding))

            current_chunk = []
            current_chunk_embeddings = []

    # Catch last chunk
    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunk_embedding = model.encode(chunk_text)
        chunks.append((chunk_text, chunk_embedding))

    # Unzip into two lists
    chunk_texts, chunk_embeddings = zip(*chunks)
    return list(chunk_texts), list(chunk_embeddings)
  

def get_chunking_params(text: str) -> dict:

    # Use sentence count to determine aggressiveness
    sentence_count = len(nltk.sent_tokenize(text))

    if sentence_count < 40:
        min_chunk_sentences = 2
        sim_threshold = 0.85
    elif sentence_count < 100:
        min_chunk_sentences = 4
        sim_threshold = 0.7
    elif sentence_count < 200:
        min_chunk_sentences = 6
        sim_threshold = 0.65
    else:
        min_chunk_sentences = 8
        sim_threshold = 0.6

    return {"min_chunk_sentences": min_chunk_sentences, "sim_threshold": sim_threshold}

if __name__ == "__main__":
    text = "Hey! My name is Pablo. I’m building an assistant to extract transcripts from YouTube and answer questions using RAG. Let’s test sentence tokenization."

    print(f"Text length: {len(text)}")

    params = get_chunking_params(text)
    print(params)

    chunk_texts, chunk_embeddings = semantic_chunks_embeddings(
        text,
        **params
    )

    for i, (text, vector) in enumerate(zip(chunk_texts, chunk_embeddings)):
        print(f"Chunk {i}: {text}")
        print(f"Vector: {vector}")
        print(f"Vector length: {vector.shape[0]}")
        print("-" * 50)
    

 

    