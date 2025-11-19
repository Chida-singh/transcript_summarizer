import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { YoutubeTranscript } from 'youtube-transcript';

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
      '/api/transcript': 'POST - Fetch transcript from YouTube URL'
    }
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

    // Fetch transcript
    const transcriptData = await YoutubeTranscript.fetchTranscript(videoId);

    if (!transcriptData || transcriptData.length === 0) {
      return res.status(404).json({
        error: 'Transcript not found',
        message: 'No transcript available for this video'
      });
    }

    // Format transcript
    const fullTranscript = transcriptData
      .map(item => item.text)
      .join(' ');

    const formattedTranscript = transcriptData.map((item, index) => ({
      index: index + 1,
      timestamp: item.offset,
      duration: item.duration,
      text: item.text
    }));

    res.json({
      success: true,
      videoId,
      url,
      transcript: {
        full: fullTranscript,
        segments: formattedTranscript,
        totalSegments: formattedTranscript.length
      }
    });

  } catch (error) {
    console.error('Error fetching transcript:', error);

    // Handle specific errors
    if (error.message.includes('Transcript is disabled')) {
      return res.status(403).json({
        error: 'Transcript disabled',
        message: 'Transcripts are disabled for this video'
      });
    }

    if (error.message.includes('Could not find')) {
      return res.status(404).json({
        error: 'Video not found',
        message: 'Could not find the video or transcript'
      });
    }

    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to fetch transcript. Please try again later.'
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
