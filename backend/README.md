# Transcript Summarizer - Backend API

A Node.js/Express backend API for fetching and processing YouTube video transcripts using YouTube's internal API.

## Features

- ✅ Fetch transcripts from YouTube videos (no API key needed!)
- ✅ Extract video ID from various YouTube URL formats
- ✅ Structured transcript data with timestamps
- ✅ Comprehensive error handling
- ✅ CORS enabled for frontend integration
- ✅ Uses YouTubei.js - YouTube's internal API wrapper

## How It Works

This backend uses **youtubei.js** library which accesses YouTube's internal API (the same API that the YouTube website uses). This means:

- ❌ **NO YouTube API key required**
- ✅ Works with any video that has captions/transcripts enabled
- ✅ More reliable than scraping methods
- ✅ Accesses the same data YouTube's website uses

## Installation

```bash
cd backend
npm install
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
PORT=3000
NODE_ENV=development
```

## Running the Server

```bash
# Development mode
npm start

# Or directly with node
node server.js
```

The server will start at `http://localhost:3000`

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
        "duration": 2.5,
        "text": "First segment text"
      },
      ...
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

### 3. Health Check
```
GET /health
```
Returns server status.

## Supported YouTube URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

## Dependencies

- **express** - Web framework
- **cors** - CORS middleware
- **youtubei.js** - YouTube's internal API wrapper (no API key needed!)
- **dotenv** - Environment variable management

## Future Enhancements

- [ ] Section-wise transcript analysis
- [ ] Context extraction and grouping
- [ ] AI-powered summarization
- [ ] Gloss format conversion
- [ ] Support for other video platforms
- [ ] Transcript caching
- [ ] Rate limiting
- [ ] Authentication

## Error Handling

The API provides detailed error messages for common issues:
- Invalid or missing URLs
- Disabled transcripts
- Video not found
- Network errors
- Server errors

## CORS

CORS is enabled for all origins in development. Configure appropriately for production.
