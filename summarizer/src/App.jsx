import { useState } from 'react'
import './App.css'

function App() {
  const [videoLink, setVideoLink] = useState('')
  const [transcript, setTranscript] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleFetchTranscript = async () => {
    if (!videoLink.trim()) {
      setError('Please enter a valid link')
      return
    }

    setLoading(true)
    setError('')
    setTranscript('')

    try {
      const response = await fetch('http://localhost:3000/api/transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: videoLink }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Failed to fetch transcript')
      }

      if (data.success && data.transcript) {
        setTranscript(data.transcript.full)
      } else {
        throw new Error('No transcript data received')
      }
      
    } catch (err) {
      setError(err.message || 'Failed to fetch transcript. Please check the link and try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setVideoLink('')
    setTranscript('')
    setError('')
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Transcript Summarizer</h1>
        <p className="subtitle">Paste a video link to extract and analyze its transcript</p>
        <p className="note">ℹ️ Note: Video must have captions/subtitles enabled</p>
      </header>

      <main className="main-content">
        <div className="input-section">
          <div className="input-group">
            <input
              type="text"
              value={videoLink}
              onChange={(e) => setVideoLink(e.target.value)}
              placeholder="Paste YouTube or video link here..."
              className="link-input"
              disabled={loading}
            />
            <div className="button-group">
              <button 
                onClick={handleFetchTranscript} 
                className="fetch-btn"
                disabled={loading || !videoLink.trim()}
              >
                {loading ? 'Fetching...' : 'Get Transcript'}
              </button>
              {(videoLink || transcript) && (
                <button 
                  onClick={handleClear} 
                  className="clear-btn"
                  disabled={loading}
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}
        </div>

        {transcript && (
          <div className="transcript-section">
            <div className="transcript-header">
              <h2>Transcript</h2>
              <span className="transcript-badge">Ready for processing</span>
            </div>
            <div className="transcript-content">
              {transcript}
            </div>
            <div className="transcript-footer">
              <p className="info-text">
                ℹ️ Next steps: This transcript will be processed for section-wise breakdown, 
                contextual analysis, summarization, and gloss format conversion.
              </p>
            </div>
          </div>
        )}

        {loading && (
          <div className="loading-section">
            <div className="spinner"></div>
            <p>Fetching transcript...</p>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Future features: Section-wise analysis • Context extraction • Summarization • Gloss format</p>
      </footer>
    </div>
  )
}

export default App
