import { useState } from "react";
import "./App.css";

/*--------------------------------------------------------------------------
  Modal - window object which represent file content.
--------------------------------------------------------------------------*/
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
  const [fileContent, setFileContent] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  /*--------------------------------------------------------------------------
    Thu function send request for fectching repo content (file names list)
  */
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

  /* --------------------------------------------------------------------------
    This function sends request for file content and update the model.
    response format:
      {
        "success": True,
          "data": {
              "content": content_response["content"],
              "type": content_response["type"],
              "extension": content_response["extension"],
              "filename": file_path
          }
      }
        or
      {
        "success": False,
        "error": e.detail
      }
  -------------------------------------------------------------------------- */
  const handleFileClick = async (file) => {
    try {
      setSelectedFile(file);
      setModalOpen(true);
      setFileContent({ type: "loading", content: "Loading..." });

      // Sends request for file content
      const response = await fetch(
        `http://localhost:8000/file-content/?repo_url=${encodeURIComponent(
          url
        )}&file_path=${encodeURIComponent(file)}`
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch file content.");
      }

      // Updates state with response data (or error)
      const data = await response.json();
      setFileContent(data.data);
    } catch (err) {
      setFileContent({
        type: "error",
        content: "Error loading file: file format is not supported",
      });
    }
  };

  /* --------------------------------------------------------------------------
    This function set the file content based on format.
  --------------------------------------------------------------------------*/
  const renderFileContent = () => {
    if (!fileContent) return null;

    if (fileContent.type === "loading") {
      return <div className="loading">Loading...</div>;
    }

    if (fileContent.type === "error") {
      return <div className="error">{fileContent.content}</div>;
    }

    if (fileContent.type === "image") {
      return (
        <div className="image-container">
          <img
            src={`data:image/${fileContent.extension};base64,${fileContent.content}`}
            alt={selectedFile}
          />
        </div>
      );
    }

    // Default foramt - text.
    return <pre className="file-content">{fileContent.content}</pre>;
  };

  // root page
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
          setFileContent(null);
        }}
      >
        {selectedFile && (
          <div className="modal-file">
            <h3>{selectedFile}</h3>
            {renderFileContent()}
          </div>
        )}
      </Modal>
    </div>
  );
}

export default App;
