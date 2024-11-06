import { useState } from "react";
import "./App.css";

function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          ×
        </button>
        {children}
      </div>
    </div>
  );
}

function App() {
  const [url, setUrl] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState("");
  const [modalOpen, setModalOpen] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setFiles([]);

    try {
      const response = await fetch(
        `http://localhost:8000/repo-files/?repo_url=${encodeURIComponent(url)}`
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || "Failed to fetch repository files."
        );
      }

      const data = await response.json();
      setFiles(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileClick = async (file) => {
    try {
      setSelectedFile(file);
      setModalOpen(true);
      setFileContent("Loading...");

      const response = await fetch(
        `http://localhost:8000/file-content/?repo_url=${encodeURIComponent(
          url
        )}&file_path=${encodeURIComponent(file)}`
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch file content.");
      }

      const data = await response.json();
      setFileContent(data.content);
    } catch (err) {
      setFileContent(`Error loading file: file format is not supported `);
    }
  };

  return (
    <div className="container">
      <h1>GitHub Repository Explorer</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter repository URL"
        />
        <button type="submit" disabled={loading || !url}>
          {loading ? "Loading..." : "Fetch Files"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}
      <div className="files-count">Total files: {files.length}</div>
      {files.length > 0 && (
        <div className="files-container">
          <h2>Repository Files:</h2>
          <ul>
            {files.map((file, index) => (
              <li
                key={index}
                onClick={() => handleFileClick(file)}
                className="file-item"
              >
                {file}
              </li>
            ))}
          </ul>
        </div>
      )}

      <Modal
        isOpen={modalOpen}
        onClose={() => {
          setModalOpen(false);
          setSelectedFile(null);
          setFileContent("");
        }}
      >
        {selectedFile && (
          <div className="modal-file">
            <h3 className="file-title">{selectedFile}</h3>
            <pre className="file-content">{fileContent}</pre>
          </div>
        )}
      </Modal>
    </div>
  );
}

export default App;
