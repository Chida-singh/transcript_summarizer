# Transcript Summarizer - Python/Flask Backend

A Python Flask backend API for fetching and processing YouTube video transcripts.

## Features

- ✅ Flask REST API server
- ✅ YouTube transcript fetching (no API key needed)
- ✅ Multiple YouTube URL format support
- ✅ Structured transcript data with timestamps
- ✅ Comprehensive error handling
- ✅ CORS enabled for frontend integration
- ✅ Ready for ML/AI feature integration

## Installation

### 1. Create Virtual Environment (Recommended)

```bash
cd backend_python
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The server will start at `http://localhost:3000`

## Environment Variables

Create a `.env` file in the backend_python directory:

```env
PORT=3000
FLASK_ENV=development
FLASK_DEBUG=True
```

## API Endpoints

### 1. Root Endpoint
```
GET /
```
Returns API information and available endpoints.

### 2. Fetch Transcript
```
POST /api/transcript
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "videoId": "VIDEO_ID",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "transcript": {
    "full": "Complete transcript text...",
    "segments": [
      {
        "index": 1,
        "timestamp": 0,
        "duration": 2500,
        "text": "First segment text"
      }
    ],
    "totalSegments": 150
  }
}
```

**Error Responses:**
- `400` - Missing or invalid URL
- `403` - Transcript disabled for video
- `404` - Video or transcript not found
- `500` - Internal server error

### 3. Check Transcript Availability
```
POST /api/check
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Returns whether a video has transcripts available.

### 4. Health Check
```
GET /health
```
Returns server status and timestamp.

## Supported YouTube URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

## Dependencies

- **Flask** - Web framework
- **flask-cors** - CORS support
- **youtube-transcript-api** - YouTube transcript fetcher
- **python-dotenv** - Environment variable management
- **gunicorn** - Production WSGI server

## Testing

Test the API with curl:

```bash
curl -X POST http://localhost:3000/api/transcript \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=LdOM0x0XDMo"}'
```

## Production Deployment

For production, use gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

## Future AI/ML Features (Ready to Add)

This Flask backend is ready for integration with:

- 🤖 Gloss format conversion
- 📊 Section-wise analysis
- 🧠 AI summarization
- 🔍 Context extraction
- 🌐 Multi-language support
- 📝 Annotation and tagging

Simply add your ML models and processing logic to the Flask app!

## Advantages of Python/Flask

- ✅ Easy ML/AI library integration (transformers, spaCy, NLTK)
- ✅ Simple and clean code
- ✅ Extensive data science ecosystem
- ✅ Easy to add NLP features
- ✅ Great for linguistic processing
