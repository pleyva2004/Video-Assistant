from pocketflow import Node, Flow, BatchNode

from data_pipeline.extractor.url_parse import get_video_id
from data_pipeline.extractor.transcript_fetcher import fetch_transcript, get_simple_text

from data_pipeline.chunker.semantic import semantic_chunks_embeddings, get_chunking_params

from data_pipeline.vector_store.create import create_collection
from data_pipeline.vector_store.upload import upload_chunks_to_qdrant
from data_pipeline.vector_store.search import query_qdrant

from llm_engineering.prompt import context_prompt, context_prompt_history
from llm_engineering.gemini_provider import GeminiClient

from qdrant_client import QdrantClient



class VideoNode(Node):
    def prep(self, shared):
        # Read the video url from the shared state
        return shared["video_url"]

    def exec(self, url):
        if url != "test":
            try: 
                video_id = get_video_id(url)
            except ValueError as e:
                print(f"Error: {e}")
                return
            
            # Fetch the transcript
            raw_data = fetch_transcript(video_id)
            text = get_simple_text(raw_data)
        else:
            print(f"\nUsing test transcript ...\n\n")
            video_id = "test"
            with open("test_transcript.txt", "r") as file:
                text = file.read()
                raw_data = None        
        return text, raw_data, video_id
        
        
    def post(self, shared, prep_result, exec_result):
        # Save the text to the shared state
        shared["video_text"] = exec_result[0]
        shared["video_raw_data"] = exec_result[1]
        shared["video_id"] = exec_result[2]

        return "default"
        
class ChunkNode(Node):
    def prep(self, shared):
        chunking_params = get_chunking_params(shared["video_text"])
        shared["chunking_params"] = chunking_params
        print(f"Chunking params: {chunking_params}")
        return shared
    
    def exec(self, shared):
        chunk_texts, chunk_embeddings = semantic_chunks_embeddings(shared["video_text"], **shared["chunking_params"])
        return chunk_texts, chunk_embeddings
    
    def post(self, shared, prep_result, exec_result):
        shared["chunk_texts"] = exec_result[0]
        shared["chunk_embeddings"] = exec_result[1]
        return "default"
    
class VectorStoreNode(Node):
    def prep(self, shared):
        shared["Qdraclient"] = QdrantClient(":memory:")
        shared["collection_name"] = "youtube_transcripts"
        shared["vector_dimension"] = shared["chunk_embeddings"][0].shape[0]
        return shared

    def exec(self, shared):

        # create the collection
        client = shared["Qdraclient"]
        collection_name = shared["collection_name"]
        vector_dimension = shared["vector_dimension"]
        video_id = shared["video_id"]
        chunk_texts = shared["chunk_texts"]
        chunk_embeddings = shared["chunk_embeddings"]

        if not client.collection_exists(collection_name):
            create_collection(client, collection_name, vector_dimension)

        # upload the chunks to the collection
        upload_chunks_to_qdrant(client, chunk_texts, chunk_embeddings, collection_name, video_id)
        return "default"
    
    def post(self, shared, prep_result, exec_result):
        if exec_result != "default":
            print ("Internal Error: VectorStoreNode exec returned non-default value")
    
        return "default"
    
class QueryNode(Node):
    def prep(self, shared):
        return shared
    
    def exec(self, shared):
        client = shared["Qdraclient"]
        collection_name = shared["collection_name"]
        query = shared["query"]

        results = query_qdrant(client, query, collection_name)
        return results

    def post(self, shared, prep_result, exec_result):
        shared["similarity_search_results"] = exec_result
        return "default"
    
class GenerateAnswerNode(Node):
    def prep(self, shared):
        shared["LLM_client"] = GeminiClient()
        return shared
    
    def exec(self, shared):
        LLM_client = shared["LLM_client"]
        similarity_search_results = shared["similarity_search_results"]
        query = shared["query"]

        prompt = context_prompt(query, similarity_search_results)
        system_prompt = "You are a helpful assistant that can answer questions based on the transcript context below. If you can't know the answer based on the context, ask if to search the web for the answer."
        answer = LLM_client.generate_text(prompt, system_prompt)
        print(f"\n\nAI: {answer}\n\n")
        return answer
    
    def post(self, shared, prep_result, exec_result):
        history = [(shared["query"], exec_result)]
        shared["history"].append(history)
        shared["query"] = input("You: ")
        return "default"
    
    

        
        
        
