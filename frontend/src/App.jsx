import { useState } from "react";
import "./App.css";

import UploadSection from "./components/UploadSection";
import ChatSection from "./components/ChatSection";

function App() {

    const [knowledgeBaseReady, setKnowledgeBaseReady] = useState(false);

    return (

        <div className="app">

            {
                knowledgeBaseReady ? (

                    <ChatSection />

                ) : (

                    <UploadSection
                        onUploadSuccess={() =>
                            setKnowledgeBaseReady(true)
                        }
                    />

                )
            }

        </div>

    );

}

export default App;