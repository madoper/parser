import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

/**
 * SEMANTIC: Main application component for web parser
 * Handles sitemap URL input and displays parsing results
 */
function App() {
  // SEMANTIC: State management for form inputs and results
  const [sitemapUrl, setSitemapUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');
  const [taskId, setTaskId] = useState('');

  /**
   * SEMANTIC: Handle form submission for sitemap parsing
   * Submit request to backend API
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResults([]);
    
    if (!sitemapUrl.trim()) {
      setError('Please enter a valid sitemap URL');
      return;
    }

    try {
      setLoading(true);
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.post(
        `${apiUrl}/api/v1/sitemap/parse`,
        { url: sitemapUrl, max_depth: 3, follow_nested: true }
      );
      
      setTaskId(response.data.task_id);
      setResults(response.data.urls || []);
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  /**
   * SEMANTIC: Fetch task status and update results
   */
  const checkTaskStatus = async () => {
    if (!taskId) return;

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.get(
        `${apiUrl}/api/v1/sitemap/task/${taskId}`
      );
      setResults(response.data.urls || []);
    } catch (err) {
      setError(`Status check failed: ${err.message}`);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Web Parser</h1>
        <p>Extract and analyze sitemap URLs</p>
      </header>
      
      <main className="App-main">
        <form onSubmit={handleSubmit} className="parser-form">
          <div className="form-group">
            <label htmlFor="url-input">Sitemap URL:</label>
            <input
              id="url-input"
              type="url"
              value={sitemapUrl}
              onChange={(e) => setSitemapUrl(e.target.value)}
              placeholder="https://example.com/sitemap.xml"
              disabled={loading}
            />
          </div>
          
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Parsing...' : 'Parse Sitemap'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}
        
        {results.length > 0 && (
          <div className="results">
            <h2>Discovered URLs ({results.length})</h2>
            <ul className="url-list">
              {results.map((url, idx) => (
                <li key={idx}>
                  <a href={url} target="_blank" rel="noopener noreferrer">
                    {url}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
