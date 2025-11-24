"""
Test script for Flask Transcript API
Run with: python test_api.py
"""

import requests
import json

API_URL = 'http://localhost:3000'

def test_root():
    """Test root endpoint"""
    print('\n' + '='*60)
    print('Testing Root Endpoint')
    print('='*60)
    
    response = requests.get(f'{API_URL}/')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')

def test_transcript(video_url):
    """Test transcript fetching"""
    print('\n' + '='*60)
    print(f'Testing Transcript Fetch')
    print('='*60)
    print(f'Video URL: {video_url}')
    
    response = requests.post(
        f'{API_URL}/api/transcript',
        json={'url': video_url},
        headers={'Content-Type': 'application/json'}
    )
    
    print(f'Status Code: {response.status_code}')
    
    if response.ok:
        data = response.json()
        print(f'✅ Success!')
        print(f'Video ID: {data["videoId"]}')
        print(f'Total Segments: {data["transcript"]["totalSegments"]}')
        print(f'Transcript Length: {len(data["transcript"]["full"])} characters')
        print(f'\nFirst 200 characters:')
        print(data["transcript"]["full"][:200] + '...')
    else:
        print(f'❌ Error: {response.json()}')

def test_check(video_url):
    """Test transcript availability check"""
    print('\n' + '='*60)
    print('Testing Transcript Check')
    print('='*60)
    print(f'Video URL: {video_url}')
    
    response = requests.post(
        f'{API_URL}/api/check',
        json={'url': video_url},
        headers={'Content-Type': 'application/json'}
    )
    
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')

if __name__ == '__main__':
    print('🧪 Testing Flask Transcript API...')
    
    # Test videos
    test_videos = [
        'https://www.youtube.com/watch?v=LdOM0x0XDMo',  # TENET trailer
        'https://www.youtube.com/watch?v=Mus_vwhTCq0',  # JavaScript tips
    ]
    
    # Test root
    test_root()
    
    # Test each video
    for video_url in test_videos:
        test_check(video_url)
        test_transcript(video_url)
    
    print('\n' + '='*60)
    print('✅ All tests completed!')
    print('='*60)
