import React, { useCallback, useEffect, useRef, useState } from 'react';
import { chatAPI } from '../services/api';
import { v4 as uuidv4 } from 'uuid';
import { FaPaperPlane, FaRobot, FaUser } from 'react-icons/fa';
import './ChatInterface.css';

function ChatInterface({ workflowId, onClose }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => uuidv4());
  const messagesEndRef = useRef(null);

  // Check if workflowId is provided
  useEffect(() => {
    if (!workflowId) {
      const errorMessage = {
        id: Date.now(),
        role: 'assistant',
        message: 'Error: No workflow selected. Please select a workflow first.',
        created_at: new Date().toISOString(),
      };
      setMessages([errorMessage]);
    }
  }, [workflowId]);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const loadChatHistory = useCallback(async () => {
    try {
      const response = await chatAPI.getHistory(sessionId);
      setMessages(response.data);
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  }, [sessionId]);

  useEffect(() => {
    loadChatHistory();
  }, [loadChatHistory]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const sendMessage = async () => {
    const trimmedMessage = inputMessage.trim();
    if (!trimmedMessage || loading || !workflowId) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      message: trimmedMessage,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage(workflowId, sessionId, trimmedMessage);
      const assistantMessage = {
        id: response.data.id,
        role: 'assistant',
        message: response.data.message,
        created_at: response.data.created_at,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now(),
        role: 'assistant',
        message: 'Error: ' + (error.response?.data?.detail || error.message),
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>GenAI Stack Chat</h2>
        {onClose && (
          <button className="close-btn" onClick={onClose}>×</button>
        )}
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-chat">
            <div className="empty-chat-title">GenAI Stack Chat</div>
            <div className="empty-chat-subtitle">Start a conversation to test your stack</div>
          </div>
        )}
        {messages.map((message) => (
          <div key={message.id} className={`chat-row ${message.role === 'user' ? 'chat-row-user' : 'chat-row-assistant'}`}>
            <div className={`chat-avatar ${message.role === 'user' ? 'chat-avatar-user' : 'chat-avatar-assistant'}`}>
              {message.role === 'user' ? <FaUser /> : <FaRobot />}
            </div>
            <div className={`chat-bubble ${message.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'}`}>
              <div className="message-content">{message.message}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-row chat-row-assistant">
            <div className="chat-avatar chat-avatar-assistant">
              <FaRobot />
            </div>
            <div className="chat-bubble chat-bubble-assistant">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input-container">
        <textarea
          className="chat-input"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={loading ? 'Thinking…' : 'Send a message'}
          rows="1"
          disabled={loading}
        />
        <button
          className="send-button"
          onClick={sendMessage}
          disabled={loading || !inputMessage.trim()}
        >
          <FaPaperPlane />
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;

