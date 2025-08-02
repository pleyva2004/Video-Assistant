# Video-Assistant Project Documentation

## Project Overview

A sophisticated YouTube video transcript processing and AI assistant system that extracts, processes, and enables intelligent Q&A interactions with video content using RAG (Retrieval Augmented Generation) architecture.

## Architecture

The project follows a clean, modular architecture with three main components:

### 1. Data Pipeline
- **URL Parsing**: Extracts YouTube video IDs from URLs
- **Transcript Extraction**: Fetches transcripts using YouTube Transcript API
- **Semantic Chunking**: Intelligently chunks text based on semantic similarity
- **Vector Storage**: Stores embeddings in Qdrant vector database

### 2. Vector Store
- **Collection Management**: Creates and manages Qdrant collections
- **Embedding Upload**: Stores text chunks with their vector embeddings
- **Similarity Search**: Retrieves relevant content based on user queries

### 3. LLM Engineering
- **Gemini Integration**: Uses Google's Gemini-1.5-flash model
- **Prompt Engineering**: Constructs context-aware prompts with conversation history
- **Conversational Interface**: Supports interactive Q&A sessions

## 🔧 Key Technologies

- **Python 3.12+** - Core language
- **Sentence Transformers** (`all-MiniLM-L6-v2`) - Text embeddings
- **Qdrant** - Vector database (in-memory for development)
- **Google Gemini AI** - Large language model
- **YouTube Transcript API** - Video transcript extraction
- **NLTK** - Natural language processing


## Main Features Implemented

### 1. URL Processing
- Regex-based YouTube URL parsing
- Video ID extraction from `watch?v=` format
- Error handling for invalid URLs

### 2. Transcript Extraction
- YouTube Transcript API integration
- Multiple output formats:
  - Simple text concatenation
  - Timestamped text
  - Duration-based text
- Robust error handling for unavailable transcripts

### 3. Intelligent Text Chunking
- **Semantic Chunking**: Uses cosine similarity between sentence embeddings
- **Adaptive Parameters**: Automatically adjusts chunking based on text length:
  - Short texts (<40 sentences): Fine-grained chunking
  - Medium texts (40-200 sentences): Balanced approach
  - Long texts (>200 sentences): Aggressive chunking
- **Configurable Thresholds**: Similarity thresholds and minimum chunk sizes

### 4. Vector Database Operations
- **Collection Creation**: Automatic Qdrant collection setup
- **Batch Upload**: Efficient embedding storage with metadata
- **Similarity Search**: Top-k retrieval with configurable parameters
- **Metadata Tracking**: Video ID, chunk index, and original text preservation

### 5. LLM Integration
- **Gemini Client**: Comprehensive Google AI integration
- **Context-Aware Prompting**: Includes relevant chunks in prompts
- **Conversation History**: Maintains context across multiple questions
- **Configurable Parameters**: Temperature, top-p, top-k settings

### 6. Interactive Chat Interface
- **Initial Question**: Automatic query processing after transcript analysis
- **Continuous Chat**: Loop-based conversation until user quits
- **Context Preservation**: Maintains conversation history for follow-up questions
- **Graceful Exit**: Simple 'q' command to terminate

## 🛠️ Advanced Features

### Smart Chunking Algorithm
```python
def semantic_chunks_embeddings(text, sim_threshold=0.7, min_chunk_sentences=4):
    # Uses sentence embeddings and cosine similarity
    # Adaptive boundary detection
    # Ensures minimum chunk sizes for context preservation
```

### Dynamic Parameter Optimization
- Sentence count analysis for optimal chunking
- Automatic threshold adjustment based on content length
- Balance between granularity and context preservation

### Robust Error Handling
- URL validation and parsing errors
- Transcript availability checking
- API key management with environment variables
- Graceful degradation for various failure modes

## 📊 Data Flow

1. **Input**: User provides YouTube URL
2. **Parse**: Extract video ID using regex
3. **Fetch**: Download transcript via YouTube API
4. **Chunk**: Semantically segment text using sentence transformers
5. **Embed**: Generate vector embeddings for each chunk
6. **Store**: Upload to Qdrant vector database with metadata
7. **Query**: Process user questions through similarity search
8. **Generate**: Create AI responses using retrieved context
9. **Interact**: Maintain conversational flow with history

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Required for Google AI access

### Dependencies
- Core ML: `sentence-transformers`, `google-generativeai`
- Vector DB: `qdrant-client`
- NLP: `nltk`
- APIs: `youtube-transcript-api`
- Utilities: `dotenv`, `openai` (backup option)

##  Usage

### Basic Operation
```bash
python main.py
# Enter YouTube URL when prompted
# Ask questions about the video content
# Type 'q' to quit
```

### Test Mode
```bash
# Use "test" as URL to use test_transcript.txt
python main.py
> Enter URL: test
```

## Development Features

- **Test Data**: Included test transcript for development
- **Memory Storage**: Uses in-memory Qdrant for development simplicity
- **Debug Options**: Commented debug prints throughout codebase
- **Modular Design**: Easy to swap components (LLM providers, vector DBs, etc.)

## Performance Optimizations

- **Batch Processing**: Efficient embedding generation
- **Vector Similarity**: Fast cosine similarity search
- **Memory Management**: In-memory vector store for quick development
- **Adaptive Chunking**: Content-length aware processing

## Key Achievements

1. **End-to-End Pipeline**: Complete YouTube → AI assistant workflow
2. **Semantic Understanding**: Context-aware text chunking and retrieval
3. **Conversational AI**: Multi-turn dialogue with memory
4. **Production-Ready Architecture**: Modular, extensible design
5. **Error Resilience**: Comprehensive error handling throughout
6. **Development Workflow**: Test data and debugging support

This project demonstrates a sophisticated understanding of:
- RAG (Retrieval Augmented Generation) architecture
- Vector databases and similarity search
- Natural language processing and embeddings
- LLM integration and prompt engineering
- Clean software architecture and modularity