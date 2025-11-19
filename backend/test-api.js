// Test script for the transcript API
// Run this with: node test-api.js

const testVideoUrl = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';

async function testAPI() {
  console.log('🧪 Testing Transcript API...\n');

  try {
    console.log('📤 Sending request to: http://localhost:3000/api/transcript');
    console.log('📹 Video URL:', testVideoUrl);
    console.log('');

    const response = await fetch('http://localhost:3000/api/transcript', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: testVideoUrl }),
    });

    const data = await response.json();

    if (response.ok) {
      console.log('✅ Success!');
      console.log('📊 Response data:');
      console.log('   - Video ID:', data.videoId);
      console.log('   - Total segments:', data.transcript.totalSegments);
      console.log('   - Transcript length:', data.transcript.full.length, 'characters');
      console.log('');
      console.log('📝 First 200 characters of transcript:');
      console.log('   ', data.transcript.full.substring(0, 200) + '...');
    } else {
      console.log('❌ Error:', data.error);
      console.log('   Message:', data.message);
    }
  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

testAPI();
