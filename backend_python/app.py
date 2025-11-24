from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import yt_dlp
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

PORT = int(os.getenv('PORT', 3000))

def extract_video_id(url):
    """
    Extract YouTube video ID from various URL formats
    """
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def fetch_transcript_ytdlp(video_id):
    """
    Fetch transcript using yt-dlp as fallback
    """
    try:
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'quiet': True,
            'no_warnings': True
        }
        
        url = f'https://www.youtube.com/watch?v={video_id}'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Try to get subtitles
            subtitles = info.get('subtitles', {}).get('en') or info.get('automatic_captions', {}).get('en')
            
            if not subtitles:
                return None
            
            # Find json3 format (contains text and timestamps)
            json_subtitle = None
            for sub in subtitles:
                if sub.get('ext') == 'json3':
                    json_subtitle = sub
                    break
            
            if not json_subtitle:
                return None
            
            # Download and parse the subtitle
            import urllib.request
            import json
            
            response = urllib.request.urlopen(json_subtitle['url'])
            subtitle_data = json.loads(response.read().decode('utf-8'))
            
            # Parse the transcript
            transcript_list = []
            if 'events' in subtitle_data:
                for event in subtitle_data['events']:
                    if 'segs' in event:
                        text = ''.join([seg.get('utf8', '') for seg in event['segs']])
                        if text.strip():
                            transcript_list.append({
                                'text': text.strip(),
                                'start': event.get('tStartMs', 0) / 1000,
                                'duration': event.get('dDurationMs', 0) / 1000
                            })
            
            return transcript_list
            
    except Exception as e:
        print(f'yt-dlp error: {str(e)}')
        return None

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Transcript Summarizer API - Python/Flask',
        'version': '2.0.0',
        'endpoints': {
            '/api/transcript': 'POST - Fetch transcript from YouTube URL',
            '/api/check': 'POST - Check if video has transcripts available'
        },
        'info': 'Videos must have captions/subtitles enabled to fetch transcripts'
    })

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    """Fetch transcript from YouTube video URL"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Please provide a YouTube URL'
            }), 400
        
        url = data['url']
        
        # Extract video ID
        video_id = extract_video_id(url)
        
        if not video_id:
            return jsonify({
                'error': 'Invalid URL',
                'message': 'Please provide a valid YouTube URL'
            }), 400
        
        print(f'Fetching transcript for video: {video_id}')
        
        # Try multiple methods to fetch transcript
        transcript_list = None
        method_used = None
        
        # Method 1: Try youtube-transcript-api first (faster)
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            method_used = 'youtube-transcript-api'
            print(f'✅ Transcript fetched using {method_used}')
        except Exception as e:
            print(f'youtube-transcript-api failed: {str(e)}')
            
            # Method 2: Fallback to yt-dlp
            print('Trying yt-dlp as fallback...')
            try:
                transcript_list = fetch_transcript_ytdlp(video_id)
                if transcript_list:
                    method_used = 'yt-dlp'
                    print(f'✅ Transcript fetched using {method_used}')
            except Exception as e2:
                print(f'yt-dlp also failed: {str(e2)}')
        
        if not transcript_list or len(transcript_list) == 0:
            return jsonify({
                'error': 'Transcript not found',
                'message': 'No transcript/captions available for this video. Make sure the video has captions enabled.'
            }), 404
        
        # Format transcript
        formatted_transcript = []
        for idx, segment in enumerate(transcript_list):
            formatted_transcript.append({
                'index': idx + 1,
                'timestamp': int(segment['start'] * 1000),  # Convert to milliseconds
                'duration': int(segment.get('duration', 0) * 1000),
                'text': segment['text']
            })
        
        full_transcript = ' '.join([seg['text'] for seg in formatted_transcript]).strip()
        
        return jsonify({
            'success': True,
            'videoId': video_id,
            'url': url,
            'method': method_used,
            'transcript': {
                'full': full_transcript,
                'segments': formatted_transcript,
                'totalSegments': len(formatted_transcript)
            }
        })
    
    except TranscriptsDisabled:
        return jsonify({
            'error': 'Transcript disabled',
            'message': 'Transcripts/captions are disabled for this video. Please try a video with captions enabled.'
        }), 403
    
    except NoTranscriptFound:
        return jsonify({
            'error': 'Transcript not available',
            'message': 'No transcript/captions found for this video. The video must have either manual captions or auto-generated captions enabled.'
        }), 404
    
    except VideoUnavailable:
        return jsonify({
            'error': 'Video not found',
            'message': 'Could not find the video. It may be private, deleted, or unavailable.'
        }), 404
    
    except Exception as e:
        print(f'Error fetching transcript: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Internal server error',
            'message': f'Failed to fetch transcript. The video may not have captions available.'
        }), 500

@app.route('/api/check', methods=['POST'])
def check_transcript():
    """Check if transcript is available for a video"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Please provide a YouTube URL'
            }), 400
        
        url = data['url']
        video_id = extract_video_id(url)
        
        if not video_id:
            return jsonify({
                'error': 'Invalid URL',
                'message': 'Please provide a valid YouTube URL'
            }), 400
        
        # Try to fetch transcript to check availability
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            has_transcript = True
            segment_count = len(transcript_list)
        except:
            # Try yt-dlp fallback
            try:
                transcript_list = fetch_transcript_ytdlp(video_id)
                has_transcript = transcript_list is not None and len(transcript_list) > 0
                segment_count = len(transcript_list) if has_transcript else 0
            except:
                has_transcript = False
                segment_count = 0
        
        return jsonify({
            'success': has_transcript,
            'videoId': video_id,
            'hasTranscript': has_transcript,
            'segmentCount': segment_count
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'hasTranscript': False,
            'error': str(e),
            'message': 'No transcript available for this video'
        })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    print(f'🚀 Flask server starting on http://localhost:{PORT}')
    print(f'📝 Environment: {os.getenv("FLASK_ENV", "development")}')
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
