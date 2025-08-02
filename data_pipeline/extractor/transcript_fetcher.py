from youtube_transcript_api import YouTubeTranscriptApi



# fetch the transcript
def fetch_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    raw_data = transcript.to_raw_data()

    return raw_data

# Simple text
def get_simple_text(raw_data):
    return " ".join([entry['text'] for entry in raw_data])

# With timestamps
def get_timestamped_text(raw_data):
    return "\n".join([f"[{entry['start']:.1f}s] {entry['text']}" for entry in raw_data])

# With duration
def get_duration_text(raw_data):
    return "\n".join([f"[{entry['start']:.1f}s - {entry['start'] + entry['duration']:.1f}s] {entry['text']}" for entry in raw_data])

# Main function
if __name__ == "__main__":
    video_id = "NpCx0qjHlBQ"
    
    raw_data = fetch_transcript(video_id)
    print(get_simple_text(raw_data))
    print(get_timestamped_text(raw_data))
    print(get_duration_text(raw_data))