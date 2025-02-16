import { useState } from 'react'
import './App.css'

function App() {
  // Track the currently selected PDF file
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  // Handle PDF file changes
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    } else {
      setSelectedFile(null)
    }
  }

  // Placeholder for your "Play" action
  const handlePlay = () => {
    alert('Playing Personal Advertisement!')
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>Personal Advertisement Launch Page</h1>
      </header>

      <main className="dashboard-main">
        {/* PDF Upload Section */}
        <section className="upload-section">
          <h2>Upload PDF</h2>
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
          />
          {selectedFile && (
            <p>
              Selected file: <strong>{selectedFile.name}</strong>
            </p>
          )}
        </section>

        {/* "Play" Section */}
        <section className="create-section">
          <h2>Play Advertisement</h2>
          <button onClick={handlePlay} className="btn-create">
            Play
          </button>
        </section>
      </main>

      <footer className="dashboard-footer">
        <p>All rights reserved - Personal Advertisement, Inc.</p>
      </footer>
    </div>
  )
}

export default App
