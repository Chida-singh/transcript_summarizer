# Backend Python Modules

## Structure

The backend has been refactored into modular components for better organization and maintainability:

### Main Application
- **`app.py`** - Flask API server with all endpoints

### Processing Modules
- **`transcript_fetcher.py`** - Fetches YouTube transcripts
  - `fetch_transcript(video_url)` - Main function to get transcripts
  - `extract_video_id(url)` - Extract video ID from URL
  - `fetch_transcript_ytdlp(video_id)` - Fallback method using yt-dlp

- **`transcript_cleaner.py`** - Cleans and formats transcripts
  - `clean_transcript(transcript_data)` - Removes timestamps, cleans text
  - Handles multiple input formats (list, dict, string)

- **`topic_segmenter.py`** - Segments text into topics
  - `segment_into_topics(sentences, num_topics)` - TF-IDF + K-Means clustering
  - `calculate_optimal_topics(text)` - Auto-calculates number of topics

- **`gloss_converter.py`** - Converts to gloss format
  - `translate_to_gloss_format(text)` - Converts text to sign language gloss
  - `convert_topics_to_gloss(topics)` - Batch conversion for topics

## API Endpoints

### POST `/api/transcript`
Fetch transcript from YouTube video
```json
{
  "videoUrl": "https://youtube.com/watch?v=..."
}
```

### POST `/api/clean`
Clean transcript text
```json
{
  "transcript": [...]  // or "full text" or {"segments": [...]}
}
```

### POST `/api/segment`
Segment into topics
```json
{
  "sentences": ["..."],
  "numTopics": 5  // optional
}
```

### POST `/api/gloss`
Convert to gloss format
```json
{
  "text": "..."  // or "topics": [...]
}
```

### POST `/api/process`
Complete pipeline (legacy)
```json
{
  "videoUrl": "...",
  "numTopics": 5  // optional
}
```

### GET `/health`
Health check

## Running

```bash
python app.py
```

Server starts on `http://localhost:3000`
