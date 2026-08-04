import { useState } from "react";
import API from "../services/api";
import Message from "./Message";

function ChatSection() {

    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    // const [sources, setSources] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {

        if (question.trim() === "") return;

        const userQuestion = question;

        setQuestion("");

        setLoading(true);

        try {

            const response = await API.post("/chat", {
                question: userQuestion
            });

            setMessages((previous) => [

                ...previous,

                {
                    role: "user",
                    text: userQuestion
                },

                {
                    role: "assistant",
                    text: response.data.answer,
                    sources: response.data.sources
                }

            ]);

        }

        catch {

            setMessages((previous) => [

                ...previous,

                {
                    role: "assistant",
                    text: "Unable to connect to backend."
                }

            ]);

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="chat-container">

            <h1>💬 Chat with your PDFs</h1>

            <p>
                Ask anything about the uploaded documents.
            </p>

            <textarea
                rows="5"
                placeholder="Ask your question..."
                value={question}
                onChange={(e) =>
                    setQuestion(e.target.value)
                }
            />

            <button
                onClick={handleSend}
                disabled={loading}
            >
                {
                    loading
                        ? "Thinking..."
                        : "Send"
                }
            </button>

            <br /><br />

            <div className="messages">

                {

                    messages.map((message, index) => (

                        <Message
                            key={index}
                            role={message.role}
                            text={message.text}
                            sources={message.sources}

                        />
                    ))
                }
            </div>
        </div>

    );

}

export default ChatSection;