function ChatInput({ question, onChange, onSend, loading }) {

    const handleKeyDown = (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            onSend();
        }
    };

    return (

        <div className="chat-input-bar">

            <div className="chat-input-inner">

                <textarea
                    rows="1"
                    placeholder="Ask something about your documents..."
                    value={question}
                    onChange={(e) => onChange(e.target.value)}
                    onKeyDown={handleKeyDown}
                />

                <button
                    className="send-btn"
                    onClick={onSend}
                    disabled={loading}
                    aria-label="Send message"
                >
                    {
                        loading
                            ? <span className="spinner"></span>
                            : "↑"
                    }
                </button>

            </div>

            <div className="chat-input-hint">
                Enter to send · Shift + Enter for a new line
            </div>

        </div>

    );

}

export default ChatInput;
