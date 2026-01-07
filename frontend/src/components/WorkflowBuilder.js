import React, {
  forwardRef,
  useCallback,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
  addEdge,
  useNodesState,
  useEdgesState,
  MarkerType,
} from 'react-flow-renderer';
import ComponentLibrary from './ComponentLibrary';
import ComponentConfigPanel from './ComponentConfigPanel';
import { workflowAPI } from '../services/api';
import { v4 as uuidv4 } from 'uuid';
import { FaCog } from 'react-icons/fa';
import './WorkflowBuilder.css';

// Node Components
function NodeHeader({ title }) {
  return (
    <div className="node-header">
      <span className="node-header-title">{title}</span>
      <span className="node-header-action">
        <FaCog />
      </span>
    </div>
  );
}

function UserQueryNode({ id, data }) {
  const query = data?.config?.query || '';

  return (
    <div className="custom-node user-query-node">
      <NodeHeader title="User Query" />

      <div className="node-body">
        <div className="node-hint">Enter point for queries</div>
        <div className="node-field">
          <div className="node-field-label">User Query</div>
          <input
            className="node-input"
            value={query}
            onChange={(e) => data?.onPatch?.(id, { query: e.target.value })}
            placeholder="Write your query here"
          />
        </div>
      </div>

      <div className="node-handle-label node-handle-label-right">Query</div>
      <Handle
        id="query"
        type="source"
        position={Position.Right}
        className="node-handle node-handle-right"
      />
    </div>
  );
}

function KnowledgeBaseNode({ id, data }) {
  const embeddingModel = data?.config?.embedding_model || 'text-embedding-3-large';
  const apiKey = data?.config?.api_key || '';
  const fileName = data?.config?.file_name || '';

  return (
    <div className="custom-node knowledgebase-node">
      <NodeHeader title="Knowledge Base" />

      <div className="node-body">
        <div className="node-hint">Let LLM search info in your file</div>

        <div className="node-field">
          <div className="node-field-label">File for Knowledge Base</div>
          <button
            type="button"
            className="node-button"
            onClick={() => data?.onUploadClick?.(id)}
          >
            {fileName ? fileName : 'Upload File'}
          </button>
        </div>

        <div className="node-field">
          <div className="node-field-label">Embedding Model</div>
          <select
            className="node-select"
            value={embeddingModel}
            onChange={(e) => data?.onPatch?.(id, { embedding_model: e.target.value })}
          >
            <option value="text-embedding-3-large">text-embedding-3-large</option>
            <option value="text-embedding-3-small">text-embedding-3-small</option>
          </select>
        </div>

        <div className="node-field">
          <div className="node-field-label">API Key</div>
          <input
            className="node-input"
            value={apiKey}
            onChange={(e) => data?.onPatch?.(id, { api_key: e.target.value })}
            placeholder="********"
          />
        </div>
      </div>

      <div className="node-handle-label node-handle-label-left">Query</div>
      <Handle
        id="query"
        type="target"
        position={Position.Left}
        className="node-handle node-handle-left"
      />

      <div className="node-handle-label node-handle-label-right">Context</div>
      <Handle
        id="context"
        type="source"
        position={Position.Right}
        className="node-handle node-handle-right"
      />
    </div>
  );
}

function LLMEngineNode({ id, data }) {
  const model = data?.config?.model || 'GPT 4o Mini';
  const apiKey = data?.config?.api_key || '';
  const prompt = data?.config?.prompt || '';
  const temperature = data?.config?.temperature ?? 0.75;
  const webSearchEnabled = !!data?.config?.web_search;
  const serpApiKey = data?.config?.serp_api_key || '';

  return (
    <div className="custom-node llm-engine-node">
      <NodeHeader title="LLM (OpenAI)" />

      <div className="node-body">
        <div className="node-hint">Run a query with OpenAI LLM</div>

        <div className="node-field">
          <div className="node-field-label">Model</div>
          <select
            className="node-select"
            value={model}
            onChange={(e) => data?.onPatch?.(id, { model: e.target.value })}
          >
            <option value="GPT 4o Mini">GPT 4o Mini</option>
            <option value="GPT-4">GPT-4</option>
            <option value="GPT-3.5">GPT-3.5</option>
          </select>
        </div>

        <div className="node-field">
          <div className="node-field-label">API Key</div>
          <input
            className="node-input"
            value={apiKey}
            onChange={(e) => data?.onPatch?.(id, { api_key: e.target.value })}
            placeholder="********"
          />
        </div>

        <div className="node-field">
          <div className="node-field-label">Prompt</div>
          <textarea
            className="node-textarea"
            value={prompt}
            onChange={(e) => data?.onPatch?.(id, { prompt: e.target.value })}
            rows={3}
            placeholder="You are a helpful assistant..."
          />
        </div>

        <div className="node-field">
          <div className="node-field-label">Temperature</div>
          <input
            className="node-range"
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={temperature}
            onChange={(e) => data?.onPatch?.(id, { temperature: Number(e.target.value) })}
          />
          <div className="node-range-value">{temperature}</div>
        </div>

        <div className="node-field node-field-row">
          <div className="node-field-label">WebSearch Tool</div>
          <label className="node-switch">
            <input
              type="checkbox"
              checked={webSearchEnabled}
              onChange={(e) => data?.onPatch?.(id, { web_search: e.target.checked })}
            />
            <span className="node-switch-slider" />
          </label>
        </div>

        {webSearchEnabled && (
          <div className="node-field">
            <div className="node-field-label">SERP API</div>
            <input
              className="node-input"
              value={serpApiKey}
              onChange={(e) => data?.onPatch?.(id, { serp_api_key: e.target.value })}
              placeholder="********"
            />
          </div>
        )}
      </div>

      <div className="node-handle-label node-handle-label-left">Context</div>
      <Handle
        id="context"
        type="target"
        position={Position.Left}
        className="node-handle node-handle-left"
      />

      <div className="node-handle-label node-handle-label-right">Output</div>
      <Handle
        id="output"
        type="source"
        position={Position.Right}
        className="node-handle node-handle-right"
      />
    </div>
  );
}

function OutputNode({ id, data }) {
  const outputText = data?.config?.output_text || '';

  return (
    <div className="custom-node output-node">
      <NodeHeader title="Output" />

      <div className="node-body">
        <div className="node-hint">Output of the result nodes as text</div>
        <div className="node-field">
          <div className="node-field-label">Output Text</div>
          <input
            className="node-input"
            value={outputText}
            onChange={(e) => data?.onPatch?.(id, { output_text: e.target.value })}
            placeholder="Output will be generated based on query"
          />
        </div>
      </div>

      <div className="node-handle-label node-handle-label-left">Output</div>
      <Handle
        id="output"
        type="target"
        position={Position.Left}
        className="node-handle node-handle-left"
      />
    </div>
  );
}

const nodeTypes = {
  user_query: UserQueryNode,
  knowledgebase: KnowledgeBaseNode,
  llm_engine: LLMEngineNode,
  output: OutputNode,
};

const initialNodes = [];
const initialEdges = [];

function getComponentLabel(type) {
  const labels = {
    user_query: 'Input',
    knowledgebase: 'Knowledge Base',
    llm_engine: 'LLM (OpenAI)',
    output: 'Output',
  };
  return labels[type] || type;
}

function mapUiModelToBackend(uiModel) {
  const mapping = {
    'GPT 4o Mini': 'gpt-4o-mini',
    'GPT-4': 'gpt-4',
    'GPT-3.5': 'gpt-3.5-turbo',
  };
  return mapping[uiModel] || uiModel || 'gpt-3.5-turbo';
}

function mapBackendModelToUi(backendModel) {
  const mapping = {
    'gpt-4o-mini': 'GPT 4o Mini',
    'gpt-4': 'GPT-4',
    'gpt-3.5-turbo': 'GPT-3.5',
  };
  return mapping[backendModel] || backendModel || 'GPT 4o Mini';
}

function mapBackendConfigToUi(type, config) {
  const safe = config || {};
  if (type === 'knowledgebase') {
    return {
      file_name: safe.file_name || '',
      embedding_model: safe.embedding_model || 'text-embedding-3-large',
      api_key: safe.api_key || '',
      embedding_provider: safe.embedding_provider || 'openai',
      collection_name: safe.collection_name || 'documents',
      n_results: safe.n_results ?? 5,
    };
  }
  if (type === 'llm_engine') {
    return {
      model: mapBackendModelToUi(safe.model),
      api_key: safe.api_key || '',
      prompt: safe.system_prompt || safe.prompt || '',
      temperature: safe.temperature ?? 0.75,
      web_search: !!safe.use_web_search,
      serp_api_key: safe.serp_api_key || '',
      max_tokens: safe.max_tokens ?? 1000,
      provider: safe.provider || 'openai',
    };
  }
  if (type === 'output') {
    return {
      output_text: safe.output_text || '',
    };
  }
  if (type === 'user_query') {
    return {
      query: safe.query || '',
    };
  }
  return safe;
}

function mapUiConfigToBackend(type, config) {
  const safe = config || {};
  if (type === 'knowledgebase') {
    return {
      embedding_provider: safe.embedding_provider || 'openai',
      collection_name: safe.collection_name || 'documents',
      n_results: safe.n_results ?? 5,
    };
  }
  if (type === 'llm_engine') {
    return {
      provider: safe.provider || 'openai',
      model: mapUiModelToBackend(safe.model),
      system_prompt: safe.prompt || '',
      use_web_search: !!safe.web_search,
      temperature: safe.temperature ?? 0.7,
      max_tokens: safe.max_tokens ?? 1000,
    };
  }
  if (type === 'user_query') {
    return {};
  }
  if (type === 'output') {
    return {};
  }
  return safe;
}

const WorkflowBuilder = forwardRef(function WorkflowBuilder(
  { onWorkflowSelect, activeWorkflow, embedded = false },
  ref
) {
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNode, setSelectedNode] = useState(null);
  const [workflowName, setWorkflowName] = useState('');
  const [workflowId, setWorkflowId] = useState(null);
  const [showSaveDialog, setShowSaveDialog] = useState(false);

  const loadWorkflow = useCallback(async (id) => {
    try {
      const response = await workflowAPI.get(id);
      const workflow = response.data;
      setWorkflowId(workflow.id);
      setWorkflowName(workflow.name);

      // Convert components to nodes
      const workflowNodes = workflow.components.map((comp) => ({
        id: comp.node_id,
        type: comp.component_type,
        position: { x: comp.position_x, y: comp.position_y },
        data: {
          label: getComponentLabel(comp.component_type),
          config: mapBackendConfigToUi(comp.component_type, comp.config || {}),
          componentId: comp.id,
        },
      }));

      // Convert connections to edges
      const workflowEdges = workflow.connections.map((conn) => {
        const sourceNode = workflow.components.find((c) => c.id === conn.source_component_id);
        const targetNode = workflow.components.find((c) => c.id === conn.target_component_id);
        return {
          id: `e${conn.id}`,
          source: sourceNode.node_id,
          target: targetNode.node_id,
          sourceHandle: conn.source_handle,
          targetHandle: conn.target_handle,
          markerEnd: {
            type: MarkerType.ArrowClosed,
          },
        };
      });

      setNodes(workflowNodes);
      setEdges(workflowEdges);
    } catch (error) {
      console.error('Error loading workflow:', error);
    }
  }, [setEdges, setNodes]);

  useEffect(() => {
    if (activeWorkflow) {
      loadWorkflow(activeWorkflow.id);
    }
  }, [activeWorkflow, loadWorkflow]);

  const patchNodeConfig = useCallback((nodeId, patch) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id !== nodeId) return node;
        const current = node.data?.config || {};
        return {
          ...node,
          data: {
            ...node.data,
            config: {
              ...current,
              ...patch,
            },
          },
        };
      })
    );
  }, [setNodes]);

  const onUploadClick = useCallback((nodeId) => {
    const input = document.getElementById(`kb-upload-${nodeId}`);
    if (input) input.click();
  }, []);

  const onUploadFile = useCallback(async (nodeId, file) => {
    if (!file) return;
    try {
      const { documentAPI } = await import('../services/api');
      await documentAPI.upload(file, nodeId);
      patchNodeConfig(nodeId, { file_name: file.name });
    } catch (e) {
      console.error('KB upload failed', e);
      patchNodeConfig(nodeId, { file_name: file.name });
    }
  }, [patchNodeConfig]);

  const nodesWithCallbacks = nodes.map((n) => {
    if (n.type !== 'knowledgebase') {
      return { ...n, data: { ...n.data, onPatch: patchNodeConfig } };
    }
    return {
      ...n,
      data: {
        ...n.data,
        onPatch: patchNodeConfig,
        onUploadClick,
        onUploadFile,
      },
    };
  });

  const onConnect = useCallback(
    (params) => {
      setEdges((eds) =>
        addEdge(
          {
            ...params,
            markerEnd: { type: MarkerType.ArrowClosed },
            style: { strokeWidth: 2 },
          },
          eds
        )
      );
    },
    [setEdges]
  );

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
  }, []);

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
  }, []);

  const addNode = useCallback((componentType, position) => {
    const newNode = {
      id: uuidv4(),
      type: componentType,
      position:
        position || {
          x: Math.random() * 400 + 100,
          y: Math.random() * 400 + 100,
        },
      data: {
        label: getComponentLabel(componentType),
        config: getDefaultConfig(componentType),
      },
    };
    setNodes((nds) => [...nds, newNode]);
  }, [setNodes]);

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const componentType = event.dataTransfer.getData('application/reactflow');

      if (!componentType || !reactFlowInstance || !reactFlowWrapper.current) return;

      const bounds = reactFlowWrapper.current.getBoundingClientRect();
      const position = reactFlowInstance.project({
        x: event.clientX - bounds.left,
        y: event.clientY - bounds.top,
      });

      addNode(componentType, position);
    },
    [addNode, reactFlowInstance]
  );

  const getDefaultConfig = (type) => {
    const configs = {
      user_query: {
        query: '',
      },
      knowledgebase: {
        file_name: '',
        embedding_model: 'text-embedding-3-large',
        api_key: '',
      },
      llm_engine: {
        model: 'GPT 4o Mini',
        api_key: '',
        prompt: '',
        temperature: 0.75,
        web_search: false,
        serp_api_key: '',
      },
      output: {
        output_text: '',
      },
    };
    return configs[type] || {};
  };

  const updateNodeConfig = (nodeId, config) => {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === nodeId ? { ...node, data: { ...node.data, config } } : node
      )
    );
    if (selectedNode && selectedNode.id === nodeId) {
      setSelectedNode({
        ...selectedNode,
        data: { ...selectedNode.data, config },
      });
    }
  };

  const saveWorkflow = async () => {
    if (!workflowName.trim()) {
      alert('Please enter a workflow name');
      return;
    }

    try {
      // Convert nodes to components
      const components = nodes.map((node) => ({
        component_type: node.type,
        node_id: node.id,
        position_x: node.position.x,
        position_y: node.position.y,
        config: mapUiConfigToBackend(node.type, node.data.config || {}),
      }));

      // Convert edges to connections - use node IDs
      const connections = edges.map((edge) => {
        return {
          source_component_id: edge.source,  // This is actually a node_id
          target_component_id: edge.target,   // This is actually a node_id
          source_handle: edge.sourceHandle,
          target_handle: edge.targetHandle,
        };
      });

      const workflowData = {
        name: workflowName,
        components,
        connections,
      };

      let response;
      if (workflowId) {
        response = await workflowAPI.update(workflowId, workflowData);
      } else {
        response = await workflowAPI.create(workflowData);
        setWorkflowId(response.data.id);
      }

      setShowSaveDialog(false);
      if (onWorkflowSelect) {
        onWorkflowSelect(response.data);
      }
      alert('Workflow saved successfully!');
    } catch (error) {
      console.error('Error saving workflow:', error);
      alert('Error saving workflow: ' + (error.response?.data?.detail || error.message));
    }
  };

  const validateWorkflow = useCallback(async () => {
    if (!workflowId) {
      alert('Please save the workflow first');
      return;
    }

    try {
      const response = await workflowAPI.validate(workflowId);
      if (response.data.valid) {
        alert('Workflow is valid!');
      } else {
        alert('Workflow validation failed: ' + response.data.error);
      }
    } catch (error) {
      console.error('Error validating workflow:', error);
      alert('Error validating workflow');
    }
  }, [workflowId]);

  const deleteNode = (nodeId) => {
    setNodes((nds) => nds.filter((node) => node.id !== nodeId));
    setEdges((eds) => eds.filter((edge) => edge.source !== nodeId && edge.target !== nodeId));
    if (selectedNode && selectedNode.id === nodeId) {
      setSelectedNode(null);
    }
  };

  useImperativeHandle(
    ref,
    () => ({
      save: () => setShowSaveDialog(true),
      validate: validateWorkflow,
    }),
    [validateWorkflow]
  );

  return (
    <div className="workflow-builder">
      <ComponentLibrary onAddNode={addNode} workflowName={workflowName} />
      
      <div
        className="workflow-canvas-container"
        ref={reactFlowWrapper}
        onDrop={onDrop}
        onDragOver={onDragOver}
      >
        {!embedded && (
          <div className="workflow-toolbar">
            <input
              type="text"
              placeholder="Workflow Name"
              value={workflowName}
              onChange={(e) => setWorkflowName(e.target.value)}
              className="workflow-name-input"
            />
            <button className="btn btn-primary" onClick={() => setShowSaveDialog(true)}>
              Save Workflow
            </button>
            <button className="btn btn-success" onClick={validateWorkflow}>
              Validate
            </button>
            {selectedNode && (
              <button
                className="btn btn-danger"
                onClick={() => deleteNode(selectedNode.id)}
              >
                Delete Node
              </button>
            )}
          </div>
        )}
        
        <ReactFlow
          nodes={nodesWithCallbacks}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          nodeTypes={nodeTypes}
          onInit={setReactFlowInstance}
          onDrop={onDrop}
          onDragOver={onDragOver}
          fitView
        >
          <Background variant="dots" gap={18} size={1} color="#d1d5db" />
          <Controls />
          {!embedded && <MiniMap />}
        </ReactFlow>

        {nodesWithCallbacks
          .filter((n) => n.type === 'knowledgebase')
          .map((n) => (
            <input
              key={n.id}
              id={`kb-upload-${n.id}`}
              type="file"
              accept=".pdf,.txt,.doc,.docx"
              style={{ display: 'none' }}
              onChange={(e) => {
                const file = e.target.files?.[0];
                n.data?.onUploadFile?.(n.id, file);
                e.target.value = '';
              }}
            />
          ))}

        {nodes.length === 0 && (
          <div className="canvas-empty">
            <div className="canvas-empty-icon">▶</div>
            <div className="canvas-empty-title">Drag & drop to get started</div>
          </div>
        )}
      </div>

      {!embedded && selectedNode && (
        <ComponentConfigPanel
          node={selectedNode}
          onConfigUpdate={updateNodeConfig}
          onClose={() => setSelectedNode(null)}
        />
      )}

      {showSaveDialog && (
        <div className="modal-overlay" onClick={() => setShowSaveDialog(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Save Workflow</h2>
            <input
              type="text"
              placeholder="Workflow Name"
              value={workflowName}
              onChange={(e) => setWorkflowName(e.target.value)}
              className="workflow-name-input"
            />
            <div className="modal-actions">
              <button className="btn btn-primary" onClick={saveWorkflow}>
                Save
              </button>
              <button className="btn btn-secondary" onClick={() => setShowSaveDialog(false)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
});

export default WorkflowBuilder;

