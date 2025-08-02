# YouTube Transcript API Functions Summary

## 📚 Available Functions

### Modern API (v1.0+) - Recommended

```python
from youtube_transcript_api import YouTubeTranscriptApi

# Create API instance
ytt_api = YouTubeTranscriptApi()

# Main methods:
transcript = ytt_api.fetch(video_id)                    # Get transcript
transcript_list = ytt_api.list(video_id)               # List all available transcripts
```

### Legacy API - Still Supported

```python
# Static methods (no instance needed):
transcript = YouTubeTranscriptApi.get_transcript(video_id)
transcripts = YouTubeTranscriptApi.get_transcripts([video_id1, video_id2])
```

## 🔧 Key Methods Reference

| Method | Type | Description | Example |
|--------|------|-------------|---------|
| `fetch(video_id)` | Instance | Get transcript for video | `api.fetch("abc123")` |
| `list(video_id)` | Instance | List available transcripts | `api.list("abc123")` |
| `get_transcript(video_id)` | Static | Legacy: Get transcript | `YouTubeTranscriptApi.get_transcript("abc123")` |
| `get_transcripts(video_ids)` | Static | Legacy: Multiple videos | `YouTubeTranscriptApi.get_transcripts(["abc", "def"])` |

## 📋 Transcript List Methods

```python
transcript_list = ytt_api.list(video_id)

# Find specific transcript types:
transcript_list.find_transcript(['en', 'es'])                    # Any transcript
transcript_list.find_manually_created_transcript(['en'])         # Manual only
transcript_list.find_generated_transcript(['en'])               # Auto-generated only
```

## 🌍 Language Support

```python
# Specify language preferences (priority order):
transcript = ytt_api.fetch(video_id, languages=['es', 'en', 'fr'])

# Translate existing transcript:
english_transcript = transcript_list.find_transcript(['en'])
spanish_transcript = english_transcript.translate('es')
```

## 📊 Data Formats

### Modern API Response (FetchedTranscript object):
```python
transcript = ytt_api.fetch(video_id)
transcript.video_id        # "abc123"
transcript.language        # "English"
transcript.language_code   # "en"
transcript.is_generated    # True/False

# Convert to raw data:
raw_data = transcript.to_raw_data()
# Returns: [{'text': 'Hello', 'start': 0.0, 'duration': 1.5}, ...]
```

### Legacy API Response (List):
```python
transcript = YouTubeTranscriptApi.get_transcript(video_id)
# Returns directly: [{'text': 'Hello', 'start': 0.0, 'duration': 1.5}, ...]
```

## ⚠️ Common Issues & Solutions

1. **AttributeError: 'YouTubeTranscriptApi' has no attribute 'get_transcript'**
   - Solution: Update to latest version or use instance methods

2. **TranscriptsDisabled**
   - Video has transcripts disabled
   - Try different video

3. **VideoUnavailable**
   - Video is private/deleted
   - Check video ID

4. **NoTranscriptFound**
   - No transcripts in requested language
   - Try `languages=['en']` or check available languages first

## 🛠️ Installation & Updates

```bash
# Install/update to latest version:
pip install --upgrade youtube-transcript-api

# Check version:
pip show youtube-transcript-api
```

## 📝 Complete Working Example

```python
from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_id):
    try:
        # Modern API approach
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=['en'])
        
        # Convert to text
        raw_data = transcript.to_raw_data()
        text = " ".join([entry['text'] for entry in raw_data])
        
        return {
            'success': True,
            'text': text,
            'language': transcript.language,
            'segments': len(raw_data)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Usage:
result = get_youtube_transcript("NpCx0qjHlBQ")
if result['success']:
    print(f"Got {result['segments']} segments in {result['language']}")
    print(result['text'][:200] + "...")
else:
    print(f"Error: {result['error']}")
```