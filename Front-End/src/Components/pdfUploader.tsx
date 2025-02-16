import { useState } from 'react'

function PdfUploader() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  // Handle PDF file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    } else {
      setSelectedFile(null)
    }
  }

  // POST the PDF to the backend when the user clicks "Generate"
  const handleGenerate = async () => {
    if (!selectedFile) {
      alert('No PDF selected.')
      return
    }

    try {
      const formData = new FormData()
      // "pdfFile" should match your backend’s expected field name
      formData.append('pdfFile', selectedFile)

      // POST request via fetch
      const response = await fetch('https://your-backend-url.com/api/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      console.log('Success:', data)
      alert('PDF successfully uploaded! Generating personal advertisement...')
    } catch (error) {
      console.error('Error uploading PDF:', error)
      alert('Error uploading PDF. Check console for details.')
    }
  }

  return (
    <div>
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

      <div className="button-group">
        {/* Generate Button (disabled until a PDF is selected) */}
        <button
          className={
            selectedFile
              ? 'btn btn-generate-ready'
              : 'btn btn-generate-disabled'
          }
          disabled={!selectedFile}
          onClick={handleGenerate}
        >
          Generate
        </button>
      </div>
    </div>
  )
}

export default PdfUploader
