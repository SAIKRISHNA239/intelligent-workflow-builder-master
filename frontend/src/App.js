import React, { useEffect, useRef, useState } from 'react';
import './App.css';
import WorkflowBuilder from './components/WorkflowBuilder';
import ChatInterface from './components/ChatInterface';
import { workflowAPI } from './services/api';
import { FaCommentDots, FaExternalLinkAlt, FaPlay, FaPlus } from 'react-icons/fa';

function App() {
  const builderRef = useRef(null);
  const [view, setView] = useState('stacks');
  const [activeWorkflow, setActiveWorkflow] = useState(null);
  const [workflows, setWorkflows] = useState([]);
  const [loadingWorkflows, setLoadingWorkflows] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newStackName, setNewStackName] = useState('');
  const [newStackDescription, setNewStackDescription] = useState('');
  const [creating, setCreating] = useState(false);

  const loadWorkflows = async () => {
    setLoadingWorkflows(true);
    try {
      const response = await workflowAPI.list();
      setWorkflows(response.data);
    } catch (error) {
      console.error('Error loading workflows:', error);
    } finally {
      setLoadingWorkflows(false);
    }
  };

  useEffect(() => {
    loadWorkflows();
  }, []);

  const openBuilder = (workflow) => {
    setActiveWorkflow(workflow);
    setView('builder');
    setShowChat(false);
  };

  const goToStacks = () => {
    setView('stacks');
    setActiveWorkflow(null);
    setShowChat(false);
  };

  const openCreateModal = () => {
    setNewStackName('');
    setNewStackDescription('');
    setShowCreateModal(true);
  };

  const createStack = async () => {
    if (!newStackName.trim() || creating) return;
    setCreating(true);
    try {
      const response = await workflowAPI.create({
        name: newStackName.trim(),
        description: newStackDescription.trim() || null,
        components: [],
        connections: [],
      });
      await loadWorkflows();
      setShowCreateModal(false);
      openBuilder(response.data);
    } catch (error) {
      console.error('Error creating workflow:', error);
      alert('Error creating stack: ' + (error.response?.data?.detail || error.message));
    } finally {
      setCreating(false);
    }
  };

  const handleSave = () => {
    builderRef.current?.save?.();
  };

  return (
    <div className="App">
      <header className="TopNav">
        <button className="TopNav-brand" onClick={goToStacks}>
          <span className="TopNav-logo">ai</span>
          <span className="TopNav-title">GenAI Stack</span>
        </button>

        <div className="TopNav-actions">
          {view === 'builder' && (
            <button className="btn btn-outline" onClick={handleSave}>
              Save
            </button>
          )}
          <div className="TopNav-avatar">S</div>
        </div>
      </header>
      
      <div className="App-content">
        {view === 'stacks' && (
          <div className="StacksPage">
            <div className="StacksHeader">
              <h2>My Stacks</h2>
              <div className="StacksHeader-spacer" />
              <button className="btn btn-success btn-icon" onClick={openCreateModal}>
                <FaPlus />
                New Stack
              </button>
            </div>

            <div className="StacksBody">
              {loadingWorkflows ? (
                <div className="StacksEmpty">
                  <div className="EmptyCard">
                    <h3>Loading…</h3>
                    <p>Please wait</p>
                  </div>
                </div>
              ) : workflows.length === 0 ? (
                <div className="StacksEmpty">
                  <div className="EmptyCard">
                    <h3>Create New Stack</h3>
                    <p>Start building your generative AI apps with our essential tools and frameworks</p>
                    <button className="btn btn-success btn-icon" onClick={openCreateModal}>
                      <FaPlus />
                      New Stack
                    </button>
                  </div>
                </div>
              ) : (
                <div className="StacksGrid">
                  {workflows.map((wf) => (
                    <div key={wf.id} className="StackCard">
                      <div className="StackCard-title">{wf.name}</div>
                      <div className="StackCard-subtitle">{wf.description || ' '}</div>
                      <div className="StackCard-actions">
                        <button className="btn btn-outline btn-icon" onClick={() => openBuilder(wf)}>
                          Edit Stack
                          <FaExternalLinkAlt />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {view === 'builder' && activeWorkflow && (
          <div className="BuilderPage">
            <WorkflowBuilder
              ref={builderRef}
              embedded
              onWorkflowSelect={(wf) => {
                setActiveWorkflow(wf);
                loadWorkflows();
              }}
              activeWorkflow={activeWorkflow}
            />

            <div className="BuilderFab">
              <button className="FabButton FabButton-play" onClick={() => builderRef.current?.validate?.()}>
                <FaPlay />
              </button>
              <button className="FabButton FabButton-chat" onClick={() => setShowChat(true)}>
                <FaCommentDots />
              </button>
            </div>

            {showChat && (
              <div className="modal-overlay" onClick={() => setShowChat(false)}>
                <div className="modal-content modal-chat" onClick={(e) => e.stopPropagation()}>
                  <ChatInterface workflowId={activeWorkflow.id} onClose={() => setShowChat(false)} />
                </div>
              </div>
            )}
          </div>
        )}

        {showCreateModal && (
          <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
            <div className="modal-content modal-create" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <div className="modal-title">Create New Stack</div>
                <button className="modal-close" onClick={() => setShowCreateModal(false)}>
                  ×
                </button>
              </div>
              <div className="modal-body">
                <div className="form-field">
                  <label>Name</label>
                  <input
                    type="text"
                    value={newStackName}
                    onChange={(e) => setNewStackName(e.target.value)}
                    placeholder=""
                  />
                </div>
                <div className="form-field">
                  <label>Description</label>
                  <textarea
                    value={newStackDescription}
                    onChange={(e) => setNewStackDescription(e.target.value)}
                    rows={5}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setShowCreateModal(false)}>
                  Cancel
                </button>
                <button
                  className="btn btn-success"
                  onClick={createStack}
                  disabled={!newStackName.trim() || creating}
                >
                  Create
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

