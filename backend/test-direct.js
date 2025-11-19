import { YoutubeTranscript } from 'youtube-transcript';

// Test with a known video that has transcripts
const testVideos = [
  'jNQXAC9IVRw', // Me at the zoo
  'dQw4w9WgXcQ', // Never Gonna Give You Up
  '9bZkp7q19f0'  // TED talk
];

async function testTranscript() {
  for (const videoId of testVideos) {
    console.log(`\n🧪 Testing video: ${videoId}`);
    console.log(`URL: https://www.youtube.com/watch?v=${videoId}`);
    
    try {
      const transcript = await YoutubeTranscript.fetchTranscript(videoId);
      console.log(`✅ SUCCESS! Found ${transcript.length} segments`);
      console.log(`First segment: ${transcript[0].text}`);
    } catch (error) {
      console.log(`❌ ERROR: ${error.message}`);
      console.log(`Full error:`, error);
    }
  }
}

testTranscript();
