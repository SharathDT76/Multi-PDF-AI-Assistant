import { useState } from "react";
import API from "../services/api";

function UploadSection({ onUploadSuccess }) {

    const [selectedFiles, setSelectedFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handleFileChange = (event) => {
        setSelectedFiles(Array.from(event.target.files));
    };

    const handleUpload = async () => {

        if (selectedFiles.length === 0) {
            setMessage("Please select at least one PDF.");
            return;
        }

        const formData = new FormData();

        selectedFiles.forEach((file) => {
            formData.append("files", file);
        });

        try {

            setLoading(true);
            setMessage("");

            const response = await API.post(
                "/upload",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            setMessage(response.data.message);

            if (response.data.success) {
                onUploadSuccess(selectedFiles);
            }

        } catch (error) {

            if (error.response) {
                setMessage(error.response.data.message);
            } else {
                setMessage("Unable to connect to backend.");
            }

        } finally {

            setLoading(false);

        }

    };

    return (

        <div className="upload-screen">

            <div className="upload-card">

                <div className="upload-mark">
                    Marginalia
                </div>

                <h1 className="upload-title">
                    Multi-PDF AI Assistant
                </h1>

                <p className="upload-subtitle">
                    Upload one or more PDF documents and chat with them using AI.
                </p>

                <label className="dropzone">

                    <input
                        type="file"
                        multiple
                        accept=".pdf"
                        onChange={handleFileChange}
                    />

                    <div className="dropzone-icon">
                        📚
                    </div>

                    <div className="dropzone-text">
                        {selectedFiles.length === 0
                            ? "Click to choose your PDF files"
                            : `${selectedFiles.length} PDF(s) selected`}
                    </div>

                    <div className="dropzone-subtext">
                        PDF files only • Multiple files supported
                    </div>

                </label>

                {selectedFiles.length > 0 && (

                    <div className="file-list">

                        {selectedFiles.map((file, index) => (

                            <div
                                key={index}
                                className="file-list-item"
                            >

                                <span className="ext">
                                    PDF
                                </span>

                                <span className="name">
                                    {file.name}
                                </span>

                            </div>

                        ))}

                    </div>

                )}

                <button
                    className="upload-btn"
                    onClick={handleUpload}
                    disabled={loading}
                >

                    {loading
                        ? "Building Knowledge Base..."
                        : "Upload PDFs"}

                </button>

                {message && (

                    <div
                        className={`upload-status ${
                            message.toLowerCase().includes("success")
                                ? "success"
                                : "error"
                        }`}
                    >
                        {message}
                    </div>

                )}

            </div>

        </div>

    );

}

export default UploadSection;