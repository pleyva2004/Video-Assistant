from flow import get_flow


def main():
    flow = get_flow()
    print("=" * 50)
    print("Video Assistant")
    print("=" * 50)
    url = input("Enter the URL of the video you want to transcribe: ")
   
    summarize = "what was the speaker’s main point?"

    shared = {
        "video_url": url,
        "query": summarize,
        "history": [],
        "video_text": None,
        "video_raw_data": None,
        "video_id": None,
        "chunking_params": None,
        "chunk_texts": None,
        "chunk_embeddings": None,
        "QdrantClient": None,  
        "collection_name": None,
        "vector_dimension": None,
        "similarity_search_results": None,
        "LLM_client": None,
    }

    flow.run(shared)

    

if __name__ == "__main__":
    main()