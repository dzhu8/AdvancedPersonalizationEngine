import PdfUploader from './Components/pdfUploader'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>Personal Advertisement</h1>
      </header>

      <main className="dashboard-main">
        <PdfUploader />
      </main>

      <footer className="dashboard-footer">
        <p>All rights reserved - Personal Advertisement, Inc.</p>
      </footer>
    </div>
  )
}

export default App
