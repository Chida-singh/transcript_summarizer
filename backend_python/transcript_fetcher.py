"""
YouTube Transcript Fetcher Module
Handles fetching transcripts from YouTube videos using multiple methods.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import yt_dlp
import re
import urllib.request
import json


def extract_video_id(url):
    """
    Extract YouTube video ID from various URL formats.
    
    Args:
        url (str): YouTube video URL
    
    Returns:
        str: Video ID or None if not found
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
    Fetch transcript using yt-dlp as fallback method.
    
    Args:
        video_id (str): YouTube video ID
    
    Returns:
        list: Transcript segments or None if failed
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


def fetch_transcript(video_url):
    """
    Main function to fetch transcript from YouTube video.
    Tries YouTubeTranscriptApi first, falls back to yt-dlp.
    
    Args:
        video_url (str): YouTube video URL
    
    Returns:
        dict: Success response with transcript data or error message
    """
    try:
        video_id = extract_video_id(video_url)
        
        if not video_id:
            return {
                'success': False,
                'error': 'Invalid YouTube URL format'
            }
        
        # Try primary method: YouTubeTranscriptApi
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            
            if transcript:
                full_transcript = ' '.join([entry['text'] for entry in transcript])
                
                return {
                    'success': True,
                    'videoId': video_id,
                    'segments': transcript,
                    'full': full_transcript,
                    'totalSegments': len(transcript),
                    'method': 'YouTubeTranscriptApi'
                }
        
        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            print(f'Primary method failed: {str(e)}, trying fallback...')
        except Exception as e:
            print(f'Primary method error (likely XML parsing issue): {str(e)}, trying fallback...')
        
        # Fallback method: yt-dlp
        transcript = fetch_transcript_ytdlp(video_id)
        
        if transcript:
            full_transcript = ' '.join([entry['text'] for entry in transcript])
            
            return {
                'success': True,
                'videoId': video_id,
                'segments': transcript,
                'full': full_transcript,
                'totalSegments': len(transcript),
                'method': 'yt-dlp'
            }
        
        return {
            'success': False,
            'error': 'No transcript available for this video. The video may not have captions enabled.'
        }
    
    except Exception as e:
        print(f'Unexpected error in fetch_transcript: {str(e)}')
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': f'Failed to fetch transcript: {str(e)}'
        }
