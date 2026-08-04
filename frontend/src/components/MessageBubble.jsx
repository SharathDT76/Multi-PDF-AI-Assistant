import SourceCard from "./SourceCard";

function MessageBubble({ role, text, sources }) {

    const isUser = role === "user";

    return (

        <div className={`message-row ${isUser ? "user" : "assistant"}`}>

            <div className="message-label">
                {isUser ? "You" : "Marginalia"}
            </div>

            <div className={`bubble ${isUser ? "user" : "assistant"}`}>
                {text}
            </div>

            {
                !isUser && sources && sources.length > 0 && (

                    <div className="sources-block">

                        <div className="sources-label">Sources</div>

                        <div className="sources-grid">
                            {
                                sources.map((source, index) => (
                                    <SourceCard
                                        key={index}
                                        source={source.source}
                                        page={source.page}
                                    />
                                ))
                            }
                        </div>

                    </div>

                )
            }

        </div>

    );

}

export default MessageBubble;
