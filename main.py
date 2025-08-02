from extractor.url_parse import get_video_id
from extractor.transcript_fetcher import fetch_transcript, get_simple_text

from chunker.semantic import semantic_chunks_embeddings, get_chunking_params


def main():
    print("Hello from video-assistant! \n\n")

    url = input("Enter the URL of the video you want to transcribe: ")
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

    # chunk the text
    params = get_chunking_params(text)
    chunks = semantic_chunks_embeddings(text, **params)
    print(f"Number of chunks: {len(chunks)}")



if __name__ == "__main__":
    main()
