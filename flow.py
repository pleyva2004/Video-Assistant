from pocketflow import Flow
from nodes import *


def get_flow():

    video_node = VideoNode()
    chunk_node = ChunkNode()
    vector_store_node = VectorStoreNode()
    query_node = QueryNode()
    generate_answer_node = GenerateAnswerNode()

    video_node >> chunk_node >> vector_store_node >> query_node >> generate_answer_node >> query_node

    myFlow = Flow(start=video_node)
    return myFlow