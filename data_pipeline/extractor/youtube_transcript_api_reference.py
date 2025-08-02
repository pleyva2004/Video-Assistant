from youtube_transcript_api import YouTubeTranscriptApi

def example_basic_usage():
    video_id = "NpCx0qjHlBQ"
    
    # Method 1: Modern API (recommended)
    print("=== Modern API ===")
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    print(f"Transcript type: {type(transcript)}")
    print(f"Video ID: {transcript.video_id}")
    print(f"Language: {transcript.language}")
    print(f"Number of segments: {len(transcript)}")
    
    # Convert to raw data
    raw_data = transcript.to_raw_data()
    print(f"First segment: {raw_data[0]}")
    
def example_list_transcripts():
    video_id = "NpCx0qjHlBQ"
    
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    
    print("=== Available Transcripts ===")
    for transcript in transcript_list:
        print(f"Language: {transcript.language} ({transcript.language_code})")
        print(f"Generated: {transcript.is_generated}")
        print(f"Translatable: {transcript.is_translatable}")
        print("---")

def example_language_preferences():
    video_id = "NpCx0qjHlBQ"
    
    # Method 1: Modern API with language preference
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=['es', 'en'])  # Spanish first, then English
    
    print(f"Retrieved language: {transcript.language}")

def example_find_specific_transcripts():
    video_id = "NpCx0qjHlBQ"
    
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    
    # Find manually created transcript
    try:
        manual_transcript = transcript_list.find_manually_created_transcript(['en'])
        print(f"Found manual transcript: {manual_transcript.language}")
    except:
        print("No manual transcript found")
    
    # Find auto-generated transcript
    try:
        auto_transcript = transcript_list.find_generated_transcript(['en'])
        print(f"Found auto-generated transcript: {auto_transcript.language}")
    except:
        print("No auto-generated transcript found")
    
    # Find any transcript
    try:
        any_transcript = transcript_list.find_transcript(['en', 'es'])
        print(f"Found transcript: {any_transcript.language}")
    except:
        print("No transcript found")

def example_translate_transcript():
    video_id = "NpCx0qjHlBQ"
    
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    
    # Get English transcript and translate to Spanish
    try:
        english_transcript = transcript_list.find_transcript(['en'])
        if english_transcript.is_translatable:
            spanish_transcript = english_transcript.translate('es')
            fetched_spanish = spanish_transcript.fetch()
            print(f"Translated to: {fetched_spanish.language}")
        else:
            print("Transcript is not translatable")
    except Exception as e:
        print(f"Translation failed: {e}")

def example_formatting_output():
    video_id = "NpCx0qjHlBQ"
    
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    raw_data = transcript.to_raw_data()
    
    # Simple text
    simple_text = " ".join([entry['text'] for entry in raw_data])
    
    # With timestamps
    timestamped_text = "\n".join([
        f"[{entry['start']:.1f}s] {entry['text']}"
        for entry in raw_data[:5]  # First 5 entries
    ])
    
    # With duration
    detailed_text = "\n".join([
        f"[{entry['start']:.1f}s - {entry['start'] + entry['duration']:.1f}s] {entry['text']}"
        for entry in raw_data[:5]  # First 5 entries
    ])
    
    print("=== Simple Text ===")
    print(simple_text[:200] + "...")
    
    print("\n=== With Timestamps ===")
    print(timestamped_text)
    
    print("\n=== With Duration ===")
    print(detailed_text)

# Main function demonstrating all features
def main():
    """Run all examples"""
    try:
        print("YouTube Transcript API Function Reference")
        print("=" * 50)
        
        example_basic_usage()
        print("\n" + "=" * 50)
        
        example_list_transcripts()
        print("\n" + "=" * 50)
        
        example_formatting_output()
        print("\n" + "=" * 50)
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")

if __name__ == "__main__":
    main()