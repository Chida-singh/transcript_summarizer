"""
Quick test for transcript fetching with fallback
"""
import requests
import json

API_URL = 'http://localhost:3000'

def test_transcript_fetch():
    """Test transcript with a popular video"""
    
    # Test with a popular video that definitely has transcripts
    test_urls = [
        'https://www.youtube.com/watch?v=LdOM0x0XDMo',  # TENET trailer
        'https://www.youtube.com/watch?v=9bZkp7q19f0',  # Popular video
    ]
    
    for url in test_urls:
        print(f'\n{"="*60}')
        print(f'Testing: {url}')
        print("="*60)
        
        try:
            response = requests.post(
                f'{API_URL}/api/transcript',
                json={'url': url},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f'Status Code: {response.status_code}')
            
            if response.ok:
                data = response.json()
                print(f'✅ SUCCESS!')
                print(f'Video ID: {data["videoId"]}')
                print(f'Total Segments: {data["transcript"]["totalSegments"]}')
                print(f'Transcript Length: {len(data["transcript"]["full"])} chars')
                print(f'\nFirst 150 characters:')
                print(f'{data["transcript"]["full"][:150]}...')
            else:
                error_data = response.json()
                print(f'❌ ERROR: {error_data.get("error")}')
                print(f'Message: {error_data.get("message")}')
                
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')

if __name__ == '__main__':
    print('🧪 Testing Flask API with fallback mechanism...\n')
    test_transcript_fetch()
    print(f'\n{"="*60}')
    print('✅ Test completed!')
    print("="*60)
