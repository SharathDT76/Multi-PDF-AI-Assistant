import { useState } from "react";

function ChatSection() {

    const [question, setQuestion] = useState("");

    const handleSend = () => {

        if (question.trim() === "") {
            return;
        }

        console.log(question);

        // Chat API will be connected here.

        setQuestion("");

    };

    return (

        <div className="chat-container">

            <h1>💬 Chat with your PDFs</h1>

            <p>
                Ask anything about the uploaded documents.
            </p>

            <textarea
                rows="6"
                value={question}
                placeholder="Ask your question..."
                onChange={(e) =>
                    setQuestion(e.target.value)
                }
            />

            <button
                onClick={handleSend}
            >
                Send
            </button>

        </div>

    );

}

export default ChatSection;