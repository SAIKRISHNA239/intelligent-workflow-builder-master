import React from 'react';
import { FaBook, FaCommentDots, FaExternalLinkAlt, FaRobot, FaSignOutAlt } from 'react-icons/fa';
import './ComponentLibrary.css';

const components = [
  { type: 'user_query', label: 'Input', Icon: FaCommentDots },
  { type: 'llm_engine', label: 'LLM (OpenAI)', Icon: FaRobot },
  { type: 'knowledgebase', label: 'Knowledge Base', Icon: FaBook },
  { type: 'output', label: 'Output', Icon: FaSignOutAlt },
];

function ComponentLibrary({ onAddNode, workflowName }) {
  const handleDragStart = (event, componentType) => {
    event.dataTransfer.setData('application/reactflow', componentType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className="component-library">
      {workflowName && (
        <div className="library-workflow">
          <button type="button" className="library-workflow-name">
            <span className="library-workflow-text">{workflowName}</span>
            <span className="library-workflow-icon">
              <FaExternalLinkAlt />
            </span>
          </button>
        </div>
      )}

      <h3>Components</h3>
      <p className="library-subtitle">Drag to add to canvas</p>
      <div className="component-list">
        {components.map((component) => (
          <div
            key={component.type}
            className="component-item"
            draggable
            onDragStart={(e) => handleDragStart(e, component.type)}
            onClick={() => onAddNode(component.type)}
          >
            <span className="component-icon"><component.Icon /></span>
            <span className="component-label">{component.label}</span>
            <span className="component-grip">≡</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ComponentLibrary;

