from data_pipeline.extractor.url_parse import get_video_id
from data_pipeline.extractor.transcript_fetcher import fetch_transcript, get_simple_text

from data_pipeline.chunker.semantic import semantic_chunks_embeddings, get_chunking_params

from data_pipeline.vector_store.create import create_collection
from data_pipeline.vector_store.upload import upload_chunks_to_qdrant
from data_pipeline.vector_store.search import query_qdrant

from llm_engineering.prompt import context_prompt, context_prompt_history
from llm_engineering.gemini_provider import GeminiClient

from qdrant_client import QdrantClient

def main():


    print("Hello from video-assistant! \n\n")

    url = input("Enter the URL of the video you want to transcribe: ")

    if url != "test":
    
        print(f"\nTranscribing video ...\n\n")


        # get the video id
        try: 
            video_id = get_video_id(url)
        except ValueError as e:
            print(f"Error: {e}")
            return



        # fetch the transcript
        raw_data = fetch_transcript(video_id)
        text = get_simple_text(raw_data)

    else:
        print(f"\nUsing test transcript ...\n\n")
        video_id = "test"
        with open("test_transcript.txt", "r") as file:
            text = file.read()

    # chunk the text
    # print(f"Chunking text ...\n\n")
    params = get_chunking_params(text)
    # print("Chunking params: ", params)

    chunk_texts, chunk_embeddings = semantic_chunks_embeddings(text, **params)
    # print(f"Number of chunks: {len(chunk_texts)}")
    # print(chunk_texts)


    # vector store
    QdrantClient = QdrantClient(":memory:")

    collection_name = "youtube_transcripts"
    query = "what was the speaker’s main point?"

    vector_dimension = chunk_embeddings[0].shape[0]

    # create the collection
    if not QdrantClient.collection_exists(collection_name):
        create_collection(QdrantClient, collection_name, vector_dimension)

    # upload the chunks to the collection
    upload_chunks_to_qdrant(QdrantClient, chunk_texts, chunk_embeddings, collection_name, video_id)

    # search the collection
    results = query_qdrant(QdrantClient, query, collection_name)

    # print(f"="*100)
    # print(f"\n\nQuery: {query}\n\n")
    # print(f"\n\nResults: \n\n")
    # for i, res in enumerate(results):
    #     # print(f"\n Match {i+1} (score: {res['score']:.3f}):")
    #     # print(res["text"])

    # ask the LLM
    client = GeminiClient()
    prompt = context_prompt(query, results)
    system_prompt = "You are a helpful assistant that can answer questions based on the transcript context below. If you can't know the answer based on the context, ask if to search the web for the answer."
    answer = client.generate_text(prompt, system_prompt)
    history = [(query, answer)]

    print(f"\n\nAI: {answer}\n\n")

    while True:
        question = input("You: ")
        if question == "q":
            print("Shutting down...")
            break 

        results = query_qdrant(QdrantClient, question, collection_name)
        prompt = context_prompt_history(question, results, history)
        answer = client.generate_text(prompt, system_prompt)
        history.append((question, answer))

        print(f"\n\nAI: {answer}\n\n")


if __name__ == "__main__":

    main()
