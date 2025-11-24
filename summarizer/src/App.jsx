import { useState } from 'react'
import './App.css'

function App() {
  const [videoLink, setVideoLink] = useState('')
  const [rawTranscript, setRawTranscript] = useState(null)
  const [cleanedTranscript, setCleanedTranscript] = useState(null)
  const [glossTranscript, setGlossTranscript] = useState(null)
  const [loading, setLoading] = useState(false)
  const [currentStep, setCurrentStep] = useState('')
  const [error, setError] = useState('')

  // Step 1: Fetch Transcript
  const handleFetchTranscript = async () => {
    if (!videoLink.trim()) {
      setError('Please enter a valid video link')
      return
    }

    setLoading(true)
    setError('')
    setCurrentStep('Fetching transcript...')

    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 60000)

      const response = await fetch('http://localhost:3000/api/transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ videoUrl: videoLink }),
        signal: controller.signal
      })

      clearTimeout(timeoutId)
      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to fetch transcript')
      }

      setRawTranscript(data)
      setCurrentStep('')
      
    } catch (err) {
      if (err.name === 'AbortError') {
        setError('Request timed out. Please try again.')
      } else {
        setError(err.message || 'Failed to fetch transcript')
      }
      setCurrentStep('')
    } finally {
      setLoading(false)
    }
  }

  // Step 2: Clean Transcript
  const handleCleanTranscript = async () => {
    if (!rawTranscript) return

    setLoading(true)
    setError('')
    setCurrentStep('Cleaning transcript...')

    try {
      const response = await fetch('http://localhost:3000/api/clean', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ transcript: rawTranscript.segments }),
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to clean transcript')
      }

      setCleanedTranscript(data)
      setCurrentStep('')
      
    } catch (err) {
      setError(err.message || 'Failed to clean transcript')
      setCurrentStep('')
    } finally {
      setLoading(false)
    }
  }

  // Step 3: Convert to Gloss
  const handleConvertToGloss = async () => {
    if (!cleanedTranscript) return

    setLoading(true)
    setError('')
    setCurrentStep('Converting to gloss format...')

    try {
      const response = await fetch('http://localhost:3000/api/gloss', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: cleanedTranscript.full_text }),
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to convert to gloss')
      }

      setGlossTranscript(data.gloss)
      setCurrentStep('')
      
    } catch (err) {
      setError(err.message || 'Failed to convert to gloss')
      setCurrentStep('')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setVideoLink('')
    setRawTranscript(null)
    setCleanedTranscript(null)
    setGlossTranscript(null)
    setError('')
    setCurrentStep('')
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🎬 Transcript to Gloss Converter</h1>
        <p className="subtitle">
          Step-by-step: Fetch → Clean → Convert to Gloss
        </p>
      </header>

      <main className="main-content">
        {/* Step 1: Input & Fetch */}
        <div className="step-section">
          <div className="step-header">
            <h2>📥 Step 1: Fetch Transcript</h2>
            {rawTranscript && <span className="step-status">✅ Complete</span>}
          </div>
          <div className="input-group">
            <input
              type="text"
              value={videoLink}
              onChange={(e) => setVideoLink(e.target.value)}
              placeholder="Paste YouTube video link here..."
              className="link-input"
              disabled={loading}
            />
            <div className="button-group">
              <button 
                onClick={handleFetchTranscript} 
                className="action-btn primary"
                disabled={loading || !videoLink.trim()}
              >
                {loading && currentStep === 'Fetching transcript...' ? '⏳ Fetching...' : '📥 Get Transcript'}
              </button>
              {rawTranscript && (
                <button 
                  onClick={handleClear} 
                  className="action-btn secondary"
                  disabled={loading}
                >
                  🔄 Start Over
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

          {rawTranscript && (
            <div className="result-box">
              <div className="result-header">
                <h3>Raw Transcript</h3>
                <div className="result-stats">
                  <span className="stat-badge">{rawTranscript.totalSegments} segments</span>
                  <button 
                    className="copy-btn-small"
                    onClick={() => copyToClipboard(rawTranscript.full)}
                  >
                    📋 Copy
                  </button>
                </div>
              </div>
              <div className="result-content">
                <p className="transcript-text">{rawTranscript.full}</p>
              </div>
            </div>
          )}
        </div>

        {/* Step 2: Clean */}
        {rawTranscript && (
          <div className="step-section">
            <div className="step-header">
              <h2>🧹 Step 2: Clean Transcript</h2>
              {cleanedTranscript && <span className="step-status">✅ Complete</span>}
            </div>
            <div className="button-group">
              <button 
                onClick={handleCleanTranscript} 
                className="action-btn primary"
                disabled={loading || cleanedTranscript}
              >
                {loading && currentStep === 'Cleaning transcript...' ? '⏳ Cleaning...' : '🧹 Clean Transcript'}
              </button>
            </div>

            {cleanedTranscript && (
              <div className="result-box">
                <div className="result-header">
                  <h3>Cleaned Transcript</h3>
                  <div className="result-stats">
                    <span className="stat-badge">{cleanedTranscript.word_count} words</span>
                    <span className="stat-badge">{cleanedTranscript.sentences.length} sentences</span>
                    <button 
                      className="copy-btn-small"
                      onClick={() => copyToClipboard(cleanedTranscript.full_text)}
                    >
                      📋 Copy
                    </button>
                  </div>
                </div>
                <div className="result-content">
                  <p className="transcript-text">{cleanedTranscript.full_text}</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Step 3: Convert to Gloss */}
        {cleanedTranscript && (
          <div className="step-section">
            <div className="step-header">
              <h2>🔤 Step 3: Convert to Gloss Format</h2>
              {glossTranscript && <span className="step-status">✅ Complete</span>}
            </div>
            <div className="button-group">
              <button 
                onClick={handleConvertToGloss} 
                className="action-btn primary"
                disabled={loading || glossTranscript}
              >
                {loading && currentStep === 'Converting to gloss format...' ? '⏳ Converting...' : '🔤 Convert to Gloss'}
              </button>
            </div>

            {glossTranscript && (
              <div className="result-box gloss-result">
                <div className="result-header">
                  <h3>Gloss Format</h3>
                  <div className="result-stats">
                    <button 
                      className="copy-btn-small"
                      onClick={() => copyToClipboard(glossTranscript)}
                    >
                      📋 Copy
                    </button>
                  </div>
                </div>
                <div className="result-content">
                  <pre className="gloss-text">{glossTranscript}</pre>
                </div>
              </div>
            )}
          </div>
        )}

        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>{currentStep}</p>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          Powered by: YouTube Transcript API • NLTK • 
          <a href="https://github.com/Chida-singh/gloss_translator" target="_blank" rel="noopener noreferrer">
            Gloss Translator
          </a>
        </p>
      </footer>
    </div>
  )
}

export default App
