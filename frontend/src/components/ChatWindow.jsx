import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

function ChatWindow({ messages, loading }) {

    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, loading]);

    return (

        <div className="chat-window">

            <div className="chat-window-inner">

                {
                    messages.length === 0 && !loading && (

                        <div className="chat-empty">
                            <div className="chat-empty-mark">📖</div>
                            <div className="chat-empty-sub">
                                Your documents are indexed and ready. Ask a question below
                                to start pulling answers straight from the pages.
                            </div>
                        </div>

                    )
                }

                {
                    messages.map((message, index) => (
                        <MessageBubble
                            key={index}
                            role={message.role}
                            text={message.text}
                            sources={message.sources}
                        />
                    ))
                }

                {
                    loading && (

                        <div className="message-row assistant">
                            <div className="message-label">Marginalia</div>
                            <div className="bubble assistant">
                                <div className="typing-dots">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </div>

                    )
                }

                <div ref={bottomRef} />

            </div>

        </div>

    );

}

export default ChatWindow;
