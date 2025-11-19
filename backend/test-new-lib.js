import { Innertube } from 'youtubei.js';

// Test with recent videos that definitely have transcripts
const testVideos = [
  { id: 'LdOM0x0XDMo', title: 'Fireship - 100 Seconds' },
  { id: 'Mus_vwhTCq0', title: 'Popular Recent Video' }
];

async function testNewLibrary() {
  console.log('🧪 Testing YouTubei.js library...\n');

  for (const video of testVideos) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`Testing: ${video.title}`);
    console.log(`Video ID: ${video.id}`);
    console.log(`URL: https://www.youtube.com/watch?v=${video.id}`);
    console.log('='.repeat(60));

    try {
      console.log('📡 Initializing Innertube...');
      const youtube = await Innertube.create();
      
      console.log('📹 Getting video info...');
      const info = await youtube.getInfo(video.id);
      console.log(`✅ Video Title: ${info.basic_info.title}`);
      
      console.log('📝 Getting transcript...');
      const transcript = await info.getTranscript();
      
      if (transcript && transcript.transcript && transcript.transcript.content) {
        const body = transcript.transcript.content.body;
        
        if (body.initial_segments) {
          const segments = body.initial_segments;
          console.log(`✅ SUCCESS! Found ${segments.length} transcript segments!`);
          console.log(`\nFirst 5 segments:`);
          segments.slice(0, 5).forEach((seg, i) => {
            const text = seg.snippet.toString();
            console.log(`${i + 1}. [${seg.start_ms}ms] ${text}`);
          });
        } else {
          console.log('❌ No initial_segments found');
        }
      } else {
        console.log('❌ No transcript found');
      }
      
    } catch (error) {
      console.error('❌ Error:', error.message);
      console.error('Full error:', error);
    }
  }
}

testNewLibrary();
