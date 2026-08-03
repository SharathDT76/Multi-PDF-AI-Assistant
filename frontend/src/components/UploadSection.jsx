import { useState } from "react";
import API from "../services/api";

function UploadSection({ onUploadSuccess }) {

    const [selectedFiles, setSelectedFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handleFileChange = (event) => {
        setSelectedFiles(event.target.files);
    };

    const handleUpload = async () => {

        if (selectedFiles.length === 0) {
            setMessage("Please select at least one PDF.");
            return;
        }

        const formData = new FormData();

        for (const file of selectedFiles) {
            formData.append("files", file);
        }

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
                onUploadSuccess();
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

        <div className="upload-container">

            <div className="upload-header">

                <img
                    src="/logo.png"
                    alt="Logo"
                    className="logo"
                />

                <h1>Multi-PDF AI Assistant</h1>

            </div>

            <p className="subtitle">
                Upload one or more PDF documents and chat with them using AI.
            </p>

            <input
                type="file"
                multiple
                accept=".pdf"
                onChange={handleFileChange}
            />

            <button
                onClick={handleUpload}
                disabled={loading}
            >
                {
                    loading
                        ? "Building Knowledge Base..."
                        : "Upload PDFs"
                }
            </button>

            {
                message &&
                <p className="message">
                    {message}
                </p>
            }

        </div>

    );

}

export default UploadSection;