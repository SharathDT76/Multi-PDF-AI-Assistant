function Message({ role, text, sources }) {

    return (

        <div
            className={
                role === "user"
                    ? "user-message"
                    : "ai-message"
            }
        >

            <strong>

                {
                    role === "user"
                        ? "👤 You"
                        : "🤖 AI"
                }

            </strong>

            <p>{text}</p>

            {

                role === "assistant"

                &&

                sources

                &&

                (

                    <div className="sources">

                        <h4>Sources</h4>

                        {

                            sources.map((source, index) => (

                                <div
                                    key={index}
                                    className="source-card"
                                >

                                    <strong>

                                        {source.source}

                                    </strong>

                                    <br />

                                    Page {source.page}

                                </div>

                            ))

                        }

                    </div>

                )

            }

        </div>

    );

}

export default Message;