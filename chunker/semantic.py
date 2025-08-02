from sentence_transformers import SentenceTransformer
from transformers import GPT2TokenizerFast
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download('punkt')

def semantic_chunks_embeddings(text, sim_threshold=0.7, min_chunk_sentences=4):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = cosine_similarity([embeddings[i-1]], [embeddings[i]])[0][0]
        print(f"Similarity between {sentences[i-1]} and {sentences[i]}: {sim}")
        print(f"Current chunk: {current_chunk}")
        print(f"Current chunk length: {len(current_chunk)}")
        current_chunk.append(sentences[i])

        # Boundary detection
        if sim < sim_threshold and len(current_chunk) >= min_chunk_sentences:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks   

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

    chunks = semantic_chunks_embeddings(
        text,
        **params
    )
    print(f"Number of chunks: {len(chunks)}")
    print(chunks)