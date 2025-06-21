import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! Ask me anything about Sixt car rentals.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setLoading(true);
    setInput('');
    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input })
      });
      const data = await res.json();
      if (data.answers && data.answers.length > 0) {
        data.answers.forEach((ans) => {
          setMessages((msgs) => [
            ...msgs,
            { sender: 'bot', text: `${ans.section}: ${ans.content}` }
          ]);
        });
      } else {
        setMessages((msgs) => [
          ...msgs,
          { sender: 'bot', text: 'Sorry, I could not find an answer.' }
        ]);
      }
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { sender: 'bot', text: 'Error connecting to backend.' }
      ]);
    }
    setLoading(false);
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-msg ${msg.sender}`}>{msg.text}</div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <form className="chat-input" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your question..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default App;
