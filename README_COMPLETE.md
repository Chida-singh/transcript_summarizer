# 🎬 Transcript Summarizer & Gloss Translator

A full-stack application that fetches YouTube transcripts, processes them using NLP, and translates them into sign language gloss format.

## ✨ Features

### Complete Processing Pipeline

1. **📥 Transcript Fetching**
   - Dual-method fallback system (youtube-transcript-api + yt-dlp)
   - Support for videos with captions/subtitles
   - Automatic retry with alternative methods

2. **🧹 Text Cleaning**
   - Removes timestamps and formatting artifacts
   - Normalizes whitespace
   - Splits into clean sentences using NLTK

3. **🔍 Topic Segmentation**
   - AI-powered topic detection using TF-IDF and K-Means clustering
   - Automatic keyword extraction for each topic
   - Configurable number of topics (2-10)
   - Intelligent grouping of related sentences

4. **🔤 Gloss Format Translation**
   - Converts English text to sign language gloss notation
   - Uses your custom [gloss_translator](https://github.com/Chida-singh/gloss_translator) package
   - Topic-by-topic translation
   - Copy-to-clipboard functionality

## 🏗️ Architecture

### Backend (Python/Flask)
- **Port:** 3000
- **Framework:** Flask 3.0.0 with CORS
- **NLP Libraries:** NLTK, scikit-learn, NumPy
- **Transcript APIs:** youtube-transcript-api, yt-dlp

### Frontend (React/Vite)
- **Port:** 5174 (dev), 5173 (prod)
- **Framework:** React 19 with Vite
- **UI Features:** Tabbed interface, real-time processing, responsive design

## 📦 Installation

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git

### Backend Setup

```bash
cd backend_python

# Create virtual environment
python -m venv ../.venv

# Activate virtual environment
# Windows:
../.venv/Scripts/activate
# Mac/Linux:
source ../.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install gloss_translator (when available)
pip install git+https://github.com/Chida-singh/gloss_translator.git
```

### Frontend Setup

```bash
cd summarizer

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🚀 Usage

### 1. Start Backend Server

```bash
cd backend_python
python app.py
```

Server will start on `http://localhost:3000`

### 2. Start Frontend

```bash
cd summarizer
npm run dev
```

Frontend will open at `http://localhost:5174`

### 3. Process a Video

1. Paste a YouTube URL with captions/subtitles
2. Set the number of topics (default: 5)
3. Click "🚀 Process Transcript"
4. View results in different tabs:
   - **Raw Transcript:** Original fetched text
   - **Cleaned Text:** Sentence-by-sentence view
   - **Topics:** AI-grouped sections with keywords
   - **Gloss Format:** Sign language gloss translations

## 📡 API Endpoints

### Complete Pipeline
```
POST /api/process
Body: { "url": "youtube_url", "num_topics": 5 }
Returns: Complete processed data with all steps
```

### Individual Operations
```
POST /api/transcript
Body: { "url": "youtube_url" }
Returns: Raw transcript

POST /api/clean
Body: { "transcript": [...] }
Returns: Cleaned text and sentences

POST /api/segment
Body: { "sentences": [...], "num_topics": 5 }
Returns: Topic-segmented sections

POST /api/gloss
Body: { "text": "english text" }
Returns: Gloss format translation

POST /api/check
Body: { "url": "youtube_url" }
Returns: Transcript availability status

GET /health
Returns: Server health status
```

## 🎨 UI Features

### Tabs Navigation
- **📄 Raw Transcript:** Full unprocessed text with word/sentence counts
- **🧹 Cleaned Text:** Numbered sentence list for easy reading
- **🔍 Topics:** Color-coded topic cards with keywords
- **🔤 Gloss Format:** Side-by-side original + gloss translation

### Interactive Elements
- Copy-to-clipboard buttons
- Real-time processing indicators
- Error handling with helpful messages
- Responsive design for mobile/tablet

## 🧪 Example Workflow

```javascript
// 1. Paste YouTube URL
"https://www.youtube.com/watch?v=dQw4w9WgXcQ"

// 2. Set topics (optional)
num_topics: 5

// 3. Process
Click "Process Transcript" button

// 4. Results
- Raw transcript: 1,234 words, 87 sentences
- Topics: 5 sections identified
- Keywords extracted for each topic
- Gloss translation for each section
```

## 📚 Dependencies

### Backend
```
Flask==3.0.0
flask-cors==4.0.0
youtube-transcript-api==0.6.1
yt-dlp==2023.12.30
nltk==3.8.1
scikit-learn==1.3.2
numpy==1.26.2
torch>=1.9.0 (for gloss_translator)
transformers>=4.18.0 (for gloss_translator)
```

### Frontend
```
react==19.0.0
react-dom==19.0.0
vite==7.2.2
```

## 🐛 Troubleshooting

### Backend Issues

**Gloss translator not working:**
```bash
# The gloss_translator package needs to be properly installed
# For now, placeholder text is shown
# Install when package structure is fixed:
pip install git+https://github.com/Chida-singh/gloss_translator.git
```

**NLTK data missing:**
```python
# Run in Python:
import nltk
nltk.download('punkt')
```

**Port 3000 already in use:**
```bash
# Change in .env file
PORT=3001
```

### Frontend Issues

**Port 5174 in use:**
```bash
# Vite will automatically try next port
# Or specify in vite.config.js
```

**CORS errors:**
```bash
# Ensure backend is running on localhost:3000
# Check CORS settings in backend/app.py
```

## 🔮 Future Enhancements

- [ ] Summarization using GPT/Claude API
- [ ] Multiple language support
- [ ] Export to PDF/DOCX
- [ ] Video timestamp linking
- [ ] Batch processing multiple videos
- [ ] User accounts and history
- [ ] Custom gloss model training interface

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use and modify

## 👤 Author

**Chida Singh**
- GitHub: [@Chida-singh](https://github.com/Chida-singh)
- Project: [transcript_summarizer](https://github.com/Chida-singh/transcript_summarizer)
- Gloss Translator: [gloss_translator](https://github.com/Chida-singh/gloss_translator)

## 🙏 Acknowledgments

- YouTube Transcript API for reliable transcript fetching
- yt-dlp for subtitle extraction fallback
- NLTK for natural language processing
- scikit-learn for topic modeling
- The sign language linguistics community

---

**Made with ❤️ for accessibility and linguistic research**
