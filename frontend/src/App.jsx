import { useState } from "react";
import "./App.css";

import API from "./services/api";

import UploadSection from "./components/UploadSection";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

function App() {

    const [knowledgeBaseReady, setKnowledgeBaseReady] = useState(false);

    const [uploadedFiles, setUploadedFiles] = useState([]);

    const [messages, setMessages] = useState([]);

    const [question, setQuestion] = useState("");

    const [loading, setLoading] = useState(false);

    const [sidebarOpen, setSidebarOpen] = useState(false);

    const handleUploadSuccess = (files) => {

        setUploadedFiles(files);

        setKnowledgeBaseReady(true);

    };

    const handleReset = () => {

        setKnowledgeBaseReady(false);

        setUploadedFiles([]);

        setMessages([]);

        setQuestion("");

    };

    const handleSend = async () => {

        if (!question.trim()) return;

        const userQuestion = question;

        setQuestion("");

        setMessages((previous) => [

            ...previous,

            {

                role: "user",

                text: userQuestion

            }

        ]);

        setLoading(true);

        try {

            const response = await API.post("/chat", {

                question: userQuestion

            });

            const assistantMessage = {

                role: "assistant",

                text: response.data.answer,

                sources: response.data.sources || []

            };

            setMessages((previous) => [

                ...previous,

                assistantMessage

            ]);

        }

        catch {

            setMessages((previous) => [

                ...previous,

                {

                    role: "assistant",

                    text: "Unable to connect to backend.",

                    sources: []

                }

            ]);

        }

        finally {

            setLoading(false);

        }

    };

    if (!knowledgeBaseReady) {

        return (

            <UploadSection

                onUploadSuccess={handleUploadSuccess}

            />

        );

    }

    return (

        <div className="app-shell">

            <Sidebar

                files={uploadedFiles}

                open={sidebarOpen}

                onClose={() => setSidebarOpen(false)}

                onReset={handleReset}

            />

            <div className="app-main">

                <Header

                    onMenu={() =>

                        setSidebarOpen(!sidebarOpen)

                    }

                />

                <ChatWindow

                    messages={messages}

                    loading={loading}

                />

                <ChatInput

                    question={question}

                    onChange={setQuestion}

                    onSend={handleSend}

                    loading={loading}

                />

            </div>

        </div>

    );

}

export default App;