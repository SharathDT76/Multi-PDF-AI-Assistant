import { useState } from 'react';
import './App.css';
import './index.css';

import API from './services/api';

import UploadSection from './components/UploadSection';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';

function App() {
  const [knowledgeBaseReady, setKnowledgeBaseReady] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploadStats, setUploadStats] = useState({ documents: 0, chunks: 0 });
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleUploadSuccess = (files, stats) => {
    setUploadedFiles(files);
    setUploadStats(stats || { documents: files.length, chunks: 0 });
    setKnowledgeBaseReady(true);
  };

  const handleReset = () => {
    setKnowledgeBaseReady(false);
    setUploadedFiles([]);
    setUploadStats({ documents: 0, chunks: 0 });
    setMessages([]);
    setQuestion('');
  };

  const handleSend = async () => {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();
    setQuestion('');
    setMessages((prev) => [...prev, { role: 'user', text: userQuestion }]);
    setLoading(true);

    try {
      const response = await API.post('/chat', { question: userQuestion });

      const assistantMessage = {
        role: 'assistant',
        text: response.data.answer || 'No answer received.',
        sources: response.data.sources || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: 'Unable to connect to the backend. Please make sure the server is running.',
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (!knowledgeBaseReady) {
    return <UploadSection onUploadSuccess={handleUploadSuccess} />;
  }

  return (
    <div className="app-shell">
      <Sidebar
        files={uploadedFiles}
        stats={uploadStats}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onReset={handleReset}
      />
      <div className="app-main">
        <Header onMenuClick={() => setSidebarOpen((prev) => !prev)} />
        <ChatWindow messages={messages} loading={loading} />
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