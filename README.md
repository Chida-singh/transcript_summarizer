# Transcript Summarizer - Full Stack Application

A modern web application for fetching, analyzing, and summarizing YouTube video transcripts.

## 📁 Project Structure

```
transcript_summarizer/
├── backend/              # Node.js/Express API server
│   ├── server.js        # Main server file
│   ├── package.json     # Backend dependencies
│   ├── .env             # Environment variables
│   ├── test-api.js      # API test script
│   └── README.md        # Backend documentation
│
└── summarizer/          # React frontend application
    ├── src/
    │   ├── App.jsx      # Main application component
    │   ├── App.css      # Application styles
    │   ├── main.jsx     # React entry point
    │   └── index.css    # Global styles
    ├── package.json     # Frontend dependencies
    └── vite.config.js   # Vite configuration
```

## 🚀 Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
# or
node server.js
```

The backend will run on `http://localhost:3000`

### Frontend Setup

1. Navigate to the summarizer directory:
```bash
cd summarizer
```

2. Install dependencies (if not already done):
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5174` (or similar)

## ✨ Current Features

### Backend (✅ Complete)
- ✅ Express.js REST API server
- ✅ YouTube transcript fetching
- ✅ Multiple YouTube URL format support
- ✅ Structured transcript data with timestamps
- ✅ Comprehensive error handling
- ✅ CORS enabled for frontend integration
- ✅ Health check endpoint

### Frontend (✅ Complete)
- ✅ Modern React application with Vite
- ✅ Clean, responsive UI design
- ✅ Video link input interface
- ✅ Real-time transcript fetching
- ✅ Loading states and animations
- ✅ Error handling and validation
- ✅ Dark/light mode support
- ✅ Mobile-responsive design

## 🎯 Future Roadmap

### Phase 1: Analysis & Processing
- [ ] **Section-wise breakdown** - Split transcript into logical sections
- [ ] **Context extraction** - Group content by themes/topics
- [ ] **Timestamp navigation** - Click timestamps to jump to video moments

### Phase 2: Summarization
- [ ] **AI-powered summarization** - Generate concise summaries
- [ ] **Key points extraction** - Highlight main ideas
- [ ] **Chapter generation** - Auto-create video chapters

### Phase 3: Gloss Format
- [ ] **Linguistic gloss conversion** - Format for linguistic analysis
- [ ] **Annotation tools** - Add custom notes and markers
- [ ] **Export options** - Download in various formats

### Phase 4: Enhancement
- [ ] **Multi-language support** - Translate transcripts
- [ ] **Search functionality** - Find specific content in transcripts
- [ ] **Save & share** - Store and share processed transcripts
- [ ] **Authentication** - User accounts and history

## 🔧 Tech Stack

### Backend
- Node.js
- Express.js
- youtube-transcript library
- CORS
- dotenv

### Frontend
- React 19
- Vite
- CSS3 with modern features
- Fetch API

## 📡 API Endpoints

### POST /api/transcript
Fetch transcript from a YouTube video URL.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "success": true,
  "videoId": "VIDEO_ID",
  "transcript": {
    "full": "Complete transcript...",
    "segments": [...],
    "totalSegments": 150
  }
}
```

## 🧪 Testing

Test the backend API:
```bash
cd backend
node test-api.js
```

## 🌟 How to Use

1. **Start both servers** (backend on :3000, frontend on :5174)
2. **Open the frontend** in your browser
3. **Paste a YouTube URL** in the input field
4. **Click "Get Transcript"** to fetch the transcript
5. **View the transcript** in the display area

## 📝 Example YouTube URLs

Try these formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## 🤝 Contributing

This is the foundation for a powerful transcript analysis tool. Future contributions welcome for:
- AI/ML integration for summarization
- Advanced text processing algorithms
- Additional video platform support
- Enhanced UI/UX features

## 📄 License

ISC

---

**Status:** ✅ Backend & Frontend operational and integrated
**Next Goal:** Implement section-wise analysis and summarization features
