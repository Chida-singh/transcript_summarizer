"""
Main Flask Application
Coordinates all transcript processing modules.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import our modular components
from transcript_fetcher import fetch_transcript
from transcript_cleaner import clean_transcript
from topic_segmenter import segment_into_topics
from gloss_converter import translate_to_gloss_format, convert_topics_to_gloss

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

PORT = int(os.getenv('PORT', 3000))


@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    """
    Fetch transcript from YouTube video URL.
    
    Request Body:
        {
            "videoUrl": "https://youtube.com/watch?v=..."
        }
    
    Returns:
        JSON with transcript segments and full text
    """
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        
        video_url = data.get('videoUrl', '').strip()
        
        if not video_url:
            print("Error: No video URL provided")
            return jsonify({
                'success': False,
                'error': 'Video URL is required'
            }), 400
        
        print(f"Fetching transcript for: {video_url}")
        result = fetch_transcript(video_url)
        
        if result['success']:
            print(f"Success! Found {result.get('totalSegments', 0)} segments")
            return jsonify(result), 200
        else:
            print(f"Failed: {result.get('error')}")
            return jsonify(result), 404
    
    except Exception as e:
        print(f'Error in /api/transcript: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/clean', methods=['POST'])
def clean():
    """
    Clean transcript text.
    
    Request Body:
        {
            "transcript": <transcript_data>
        }
        
        transcript_data can be:
        - List of segments: [{"text": "...", "start": 0, "duration": 1}, ...]
        - Dict with segments: {"segments": [...]}
        - Dict with full text: {"full": "..."}
        - String: "full text here"
    
    Returns:
        JSON with cleaned text, sentences, and word count
    """
    try:
        data = request.get_json()
        transcript_data = data.get('transcript')
        
        if not transcript_data:
            return jsonify({
                'success': False,
                'error': 'Transcript data is required'
            }), 400
        
        print(f"Received transcript type: {type(transcript_data)}")
        print(f"Transcript data preview: {str(transcript_data)[:200]}...")
        
        result = clean_transcript(transcript_data)
        
        if result:
            return jsonify({
                'success': True,
                **result
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to clean transcript. Please check the input format.'
            }), 400
    
    except Exception as e:
        print(f'Error in /api/clean: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/segment', methods=['POST'])
def segment():
    """
    Segment cleaned text into topics.
    
    Request Body:
        {
            "sentences": ["sentence 1", "sentence 2", ...],
            "numTopics": 5  // optional, will auto-calculate if not provided
        }
    
    Returns:
        JSON with topic sections
    """
    try:
        data = request.get_json()
        sentences = data.get('sentences', [])
        num_topics = data.get('numTopics')
        
        if not sentences:
            return jsonify({
                'success': False,
                'error': 'Sentences are required'
            }), 400
        
        topics = segment_into_topics(sentences, num_topics)
        
        return jsonify({
            'success': True,
            'topics': topics,
            'numTopics': len(topics)
        }), 200
    
    except Exception as e:
        print(f'Error in /api/segment: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/gloss', methods=['POST'])
def gloss():
    """
    Convert text to gloss format.
    
    Request Body:
        {
            "text": "text to convert"
        }
        OR
        {
            "topics": [{"text": "...", ...}, ...]
        }
    
    Returns:
        JSON with gloss translation
    """
    try:
        data = request.get_json()
        
        # Handle single text conversion
        if 'text' in data:
            text = data.get('text', '')
            
            if not text:
                return jsonify({
                    'success': False,
                    'error': 'Text is required'
                }), 400
            
            gloss_text = translate_to_gloss_format(text)
            
            return jsonify({
                'success': True,
                'gloss': gloss_text
            }), 200
        
        # Handle topics conversion
        elif 'topics' in data:
            topics = data.get('topics', [])
            
            if not topics:
                return jsonify({
                    'success': False,
                    'error': 'Topics are required'
                }), 400
            
            topics_with_gloss = convert_topics_to_gloss(topics)
            
            return jsonify({
                'success': True,
                'topics': topics_with_gloss
            }), 200
        
        else:
            return jsonify({
                'success': False,
                'error': 'Either "text" or "topics" is required'
            }), 400
    
    except Exception as e:
        print(f'Error in /api/gloss: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/process', methods=['POST'])
def process():
    """
    Complete processing pipeline: fetch → clean → segment → gloss.
    (Legacy endpoint for backwards compatibility)
    
    Request Body:
        {
            "videoUrl": "https://youtube.com/watch?v=...",
            "numTopics": 5  // optional
        }
    
    Returns:
        JSON with all processed data
    """
    try:
        data = request.get_json()
        video_url = data.get('videoUrl', '').strip()
        num_topics = data.get('numTopics')
        
        if not video_url:
            return jsonify({
                'success': False,
                'error': 'Video URL is required'
            }), 400
        
        # Step 1: Fetch transcript
        transcript_result = fetch_transcript(video_url)
        if not transcript_result['success']:
            return jsonify(transcript_result), 404
        
        # Step 2: Clean transcript
        cleaned = clean_transcript(transcript_result['segments'])
        if not cleaned:
            return jsonify({
                'success': False,
                'error': 'Failed to clean transcript'
            }), 500
        
        # Step 3: Segment into topics
        topics = segment_into_topics(cleaned['sentences'], num_topics)
        
        # Step 4: Convert to gloss
        topics_with_gloss = convert_topics_to_gloss(topics)
        
        return jsonify({
            'success': True,
            'rawTranscript': transcript_result,
            'cleanedData': cleaned,
            'topics': topics_with_gloss
        }), 200
    
    except Exception as e:
        print(f'Error in /api/process: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Transcript Processor API is running'
    }), 200


if __name__ == '__main__':
    print('=' * 50)
    print('🚀 Flask server starting on http://localhost:3000')
    print('📝 Environment: development')
    print('=' * 50)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=PORT)
