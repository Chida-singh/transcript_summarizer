"""
LLM-Based Topic Segmentation (Optional Enhancement)
Uses AI APIs to intelligently segment transcripts.
"""

import os
import json


def segment_with_gemini(text, num_topics=None):
    """
    Segment transcript using Google Gemini.
    
    Args:
        text (str): Full transcript text
        num_topics (int, optional): Desired number of topics
    
    Returns:
        list: Topic sections with intelligent segmentation
    """
    try:
        import google.generativeai as genai
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment")
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Build prompt
        prompt = f"""Analyze this video transcript and divide it into {num_topics or 'meaningful'} distinct topic sections.

For each topic, provide:
1. A clear topic name (2-5 words)
2. 3 relevant keywords
3. The transcript text for that section

Return ONLY a JSON array with this structure:
[{{"topic_name": "Topic Name", "keywords": ["keyword1", "keyword2", "keyword3"], "text": "transcript text for this topic"}}]

Transcript:
{text}"""

        response = model.generate_content(prompt)
        result = response.text
        
        # Try to extract JSON
        if '```json' in result:
            result = result.split('```json')[1].split('```')[0]
        elif '```' in result:
            result = result.split('```')[1].split('```')[0]
        
        result = result.strip()
        topics = json.loads(result)
        
        # Format to match our structure
        formatted_topics = []
        for i, topic in enumerate(topics):
            formatted_topics.append({
                'topic_id': i,
                'topic_name': topic.get('topic_name', f'Topic {i+1}'),
                'keywords': topic.get('keywords', []),
                'text': topic.get('text', ''),
                'sentences': topic.get('text', '').split('. ')
            })
        
        print(f"Gemini segmented into {len(formatted_topics)} topics")
        return formatted_topics
        
    except ImportError:
        print("Google Generative AI package not installed. Run: pip install google-generativeai")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse Gemini response as JSON: {str(e)}")
        print(f"Response was: {result[:200]}...")
        return None
    except Exception as e:
        print(f"Error in Gemini segmentation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def segment_with_openai(text, num_topics=None):
    """
    Segment transcript using OpenAI GPT.
    
    Args:
        text (str): Full transcript text
        num_topics (int, optional): Desired number of topics
    
    Returns:
        list: Topic sections with intelligent segmentation
    """
    try:
        import openai
        
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in environment")
            return None
        
        openai.api_key = api_key
        
        # Build prompt
        prompt = f"""Analyze this video transcript and divide it into {num_topics or 'meaningful'} distinct topic sections.

For each topic, provide:
1. A clear topic name (2-5 words)
2. 3 relevant keywords
3. The transcript text for that section

Return as JSON array: [{{"topic_name": "...", "keywords": ["...", "...", "..."], "text": "..."}}]

Transcript:
{text[:4000]}"""  # Limit to avoid token limits

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a video content analyzer specializing in topic segmentation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Parse response
        result = response.choices[0].message.content
        
        # Try to extract JSON
        if '```json' in result:
            result = result.split('```json')[1].split('```')[0]
        elif '```' in result:
            result = result.split('```')[1].split('```')[0]
        
        topics = json.loads(result)
        
        # Format to match our structure
        formatted_topics = []
        for i, topic in enumerate(topics):
            formatted_topics.append({
                'topic_id': i,
                'topic_name': topic.get('topic_name', f'Topic {i+1}'),
                'keywords': topic.get('keywords', []),
                'text': topic.get('text', ''),
                'sentences': topic.get('text', '').split('. ')
            })
        
        return formatted_topics
        
    except ImportError:
        print("OpenAI package not installed. Run: pip install openai")
        return None
    except Exception as e:
        print(f"Error in LLM segmentation: {str(e)}")
        return None


def segment_with_claude(text, num_topics=None):
    """
    Segment transcript using Anthropic Claude.
    
    Args:
        text (str): Full transcript text
        num_topics (int, optional): Desired number of topics
    
    Returns:
        list: Topic sections
    """
    try:
        import anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("Warning: ANTHROPIC_API_KEY not found")
            return None
        
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Divide this transcript into {num_topics or 'logical'} topic sections. 
                
Return JSON: [{{"topic_name": "...", "keywords": [...], "text": "..."}}]

Transcript: {text[:4000]}"""
            }]
        )
        
        result = message.content[0].text
        
        # Parse JSON
        if '```json' in result:
            result = result.split('```json')[1].split('```')[0]
        
        topics = json.loads(result)
        
        # Format
        formatted_topics = []
        for i, topic in enumerate(topics):
            formatted_topics.append({
                'topic_id': i,
                'topic_name': topic.get('topic_name', f'Topic {i+1}'),
                'keywords': topic.get('keywords', []),
                'text': topic.get('text', ''),
                'sentences': topic.get('text', '').split('. ')
            })
        
        return formatted_topics
        
    except ImportError:
        print("Anthropic package not installed. Run: pip install anthropic")
        return None
    except Exception as e:
        print(f"Error in Claude segmentation: {str(e)}")
        return None


# Default to Gemini (free and fast)
def segment_with_llm(text, num_topics=None, provider='gemini'):
    """
    Segment transcript using any available LLM.
    
    Args:
        text (str): Full transcript text
        num_topics (int, optional): Desired number of topics
        provider (str): 'gemini', 'openai', or 'claude'
    
    Returns:
        list: Topic sections
    """
    if provider == 'gemini':
        return segment_with_gemini(text, num_topics)
    elif provider == 'openai':
        return segment_with_openai(text, num_topics)
    elif provider == 'claude':
        return segment_with_claude(text, num_topics)
    else:
        print(f"Unknown provider: {provider}")
        return None
