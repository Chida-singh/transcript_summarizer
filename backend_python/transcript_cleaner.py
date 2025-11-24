"""
Transcript Cleaner Module
Handles cleaning and processing of raw transcripts.
"""

import re
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt tokenizer...")
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading punkt_tab tokenizer...")
    nltk.download('punkt_tab', quiet=True)


def clean_transcript(transcript_data):
    """
    Clean the transcript by removing timestamps and formatting properly.
    Handles multiple input formats from the frontend.
    
    Args:
        transcript_data (list, dict, or str): Raw transcript data
    
    Returns:
        dict: Cleaned transcript with full_text, sentences, and word_count
              or None if cleaning fails
    """
    try:
        full_text = ""
        
        # Handle different input formats
        if isinstance(transcript_data, str):
            # Direct string input
            full_text = transcript_data
            
        elif isinstance(transcript_data, dict):
            # Dictionary with 'segments' key (from fetch endpoint)
            if 'segments' in transcript_data:
                segments = transcript_data['segments']
                if isinstance(segments, list):
                    full_text = ' '.join([
                        entry.get('text', '') 
                        for entry in segments 
                        if isinstance(entry, dict)
                    ])
                else:
                    full_text = str(segments)
            
            # Dictionary with 'full' key
            elif 'full' in transcript_data:
                full_text = transcript_data['full']
            
            # Dictionary with 'text' key (single segment)
            elif 'text' in transcript_data:
                full_text = transcript_data['text']
            
            # Unknown dict format
            else:
                print(f"Unknown dict format with keys: {transcript_data.keys()}")
                return None
        
        elif isinstance(transcript_data, list):
            # List of transcript segments
            full_text = ' '.join([
                entry.get('text', '') if isinstance(entry, dict) else str(entry)
                for entry in transcript_data
            ])
        
        else:
            print(f"Unsupported transcript type: {type(transcript_data)}")
            return None
        
        # Validate we have text
        if not full_text or not full_text.strip():
            print("No text content found in transcript")
            return None
        
        # Clean the text
        # Remove extra whitespace
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        
        # Remove conversation markers (>>)
        full_text = re.sub(r'>>\s*', '', full_text)
        
        # Remove [Music], [Applause], etc.
        full_text = re.sub(r'\[.*?\]', '', full_text)
        
        # Remove multiple punctuation
        full_text = re.sub(r'([.!?])\1+', r'\1', full_text)
        
        # Split into sentences
        sentences = sent_tokenize(full_text)
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        result = {
            'full_text': full_text,
            'sentences': sentences,
            'word_count': len(full_text.split()),
            'sentence_count': len(sentences)
        }
        
        print(f"Successfully cleaned transcript: {result['word_count']} words, {result['sentence_count']} sentences")
        return result
        
    except Exception as e:
        print(f"Error cleaning transcript: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
