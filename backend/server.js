import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { Innertube } from 'youtubei.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Helper function to extract YouTube video ID from URL
function extractVideoId(url) {
  const patterns = [
    /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)/,
    /(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)/,
    /(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)/,
    /(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^?]+)/
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match && match[1]) {
      return match[1];
    }
  }

  return null;
}

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Transcript Summarizer API',
    version: '1.0.0',
    endpoints: {
      '/api/transcript': 'POST - Fetch transcript from YouTube URL',
      '/api/check': 'POST - Check if video has transcripts available'
    },
    info: 'Videos must have captions/subtitles enabled to fetch transcripts'
  });
});

app.post('/api/transcript', async (req, res) => {
  try {
    const { url } = req.body;

    if (!url) {
      return res.status(400).json({
        error: 'Missing required field',
        message: 'Please provide a YouTube URL'
      });
    }

    // Extract video ID from URL
    const videoId = extractVideoId(url);
    
    if (!videoId) {
      return res.status(400).json({
        error: 'Invalid URL',
        message: 'Please provide a valid YouTube URL'
      });
    }

    console.log(`Fetching transcript for video: ${videoId}`);

    // Initialize Innertube
    const youtube = await Innertube.create();
    
    // Get video info
    const info = await youtube.getInfo(videoId);
    
    // Get transcript
    const transcriptData = await info.getTranscript();
    
    if (!transcriptData || !transcriptData.transcript || !transcriptData.transcript.content) {
      return res.status(404).json({
        error: 'Transcript not found',
        message: 'No transcript/captions available for this video. Make sure the video has captions enabled.'
      });
    }

    // Extract transcript segments from the proper structure
    const transcriptContent = transcriptData.transcript.content;
    const segmentList = transcriptContent.body;
    
    if (!segmentList || !segmentList.initial_segments) {
      return res.status(404).json({
        error: 'Transcript not found',
        message: 'No transcript segments found for this video'
      });
    }

    const segments = segmentList.initial_segments;

    // Format transcript
    const formattedTranscript = segments.map((segment, index) => {
      // Extract text from the Text object
      const text = segment.snippet.toString();
      return {
        index: index + 1,
        timestamp: parseInt(segment.start_ms),
        duration: parseInt(segment.end_ms) - parseInt(segment.start_ms),
        text: text
      };
    });

    const fullTranscript = formattedTranscript
      .map(item => item.text)
      .join(' ')
      .trim();

    res.json({
      success: true,
      videoId,
      url,
      videoTitle: info.basic_info.title,
      transcript: {
        full: fullTranscript,
        segments: formattedTranscript,
        totalSegments: formattedTranscript.length
      }
    });

  } catch (error) {
    console.error('Error fetching transcript:', error);
    console.error('Error details:', error.message);

    // Handle specific errors
    if (error.message.includes('Transcript is disabled') || error.message.includes('disabled')) {
      return res.status(403).json({
        error: 'Transcript disabled',
        message: 'Transcripts/captions are disabled for this video. Please try a video with captions enabled.'
      });
    }

    if (error.message.includes('Could not find') || error.message.includes('not available') || error.message.includes('No transcript')) {
      return res.status(404).json({
        error: 'Transcript not available',
        message: 'No transcript/captions found for this video. The video must have either manual captions or auto-generated captions enabled.'
      });
    }

    if (error.message.includes('Too Many Requests') || error.message.includes('rate limit')) {
      return res.status(429).json({
        error: 'Rate limit exceeded',
        message: 'Too many requests. Please wait a moment and try again.'
      });
    }

    res.status(500).json({
      error: 'Internal server error',
      message: `Failed to fetch transcript: ${error.message}`
    });
  }
});

// Check if transcript is available (without fetching full transcript)
app.post('/api/check', async (req, res) => {
  try {
    const { url } = req.body;

    if (!url) {
      return res.status(400).json({
        error: 'Missing required field',
        message: 'Please provide a YouTube URL'
      });
    }

    const videoId = extractVideoId(url);
    
    if (!videoId) {
      return res.status(400).json({
        error: 'Invalid URL',
        message: 'Please provide a valid YouTube URL'
      });
    }

    // Initialize Innertube and check for transcript
    const youtube = await Innertube.create();
    const info = await youtube.getInfo(videoId);
    const transcriptData = await info.getTranscript();

    const hasTranscript = transcriptData && transcriptData.transcript && transcriptData.transcript.content;
    let segmentCount = 0;
    
    if (hasTranscript) {
      const segmentList = transcriptData.transcript.content.body;
      segmentCount = segmentList && segmentList.initial_segments ? segmentList.initial_segments.length : 0;
    }

    res.json({
      success: true,
      videoId,
      hasTranscript,
      segmentCount,
      videoTitle: info.basic_info.title
    });

  } catch (error) {
    res.json({
      success: false,
      hasTranscript: false,
      error: error.message,
      message: 'No transcript available for this video'
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: 'The requested endpoint does not exist'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`📝 Environment: ${process.env.NODE_ENV || 'development'}`);
});
