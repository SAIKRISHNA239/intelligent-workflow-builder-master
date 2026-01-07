"""
Workflow execution service
"""
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.models.workflow import Workflow, WorkflowComponent, ComponentConnection
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStoreService


class WorkflowExecutor:
    """Service for executing workflows"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()
    
    def validate_workflow(self, workflow: Workflow) -> tuple[bool, Optional[str]]:
        """
        Validate workflow structure
        
        Args:
            workflow: Workflow to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        components = workflow.components
        
        # Check for required components
        component_types = [c.component_type for c in components]
        
        if "user_query" not in component_types:
            return False, "Workflow must contain a User Query component"
        
        if "llm_engine" not in component_types:
            return False, "Workflow must contain an LLM Engine component"
        
        if "output" not in component_types:
            return False, "Workflow must contain an Output component"
        
        # Check for valid connections
        connections = workflow.connections
        component_ids = {c.id for c in components}
        
        for conn in connections:
            if conn.source_component_id not in component_ids:
                return False, f"Connection references invalid source component: {conn.source_component_id}"
            if conn.target_component_id not in component_ids:
                return False, f"Connection references invalid target component: {conn.target_component_id}"
        
        # Check that user_query is connected
        user_query_component = next((c for c in components if c.component_type == "user_query"), None)
        if user_query_component:
            has_outgoing = any(c.source_component_id == user_query_component.id for c in connections)
            if not has_outgoing:
                return False, "User Query component must have outgoing connections"
        
        # Check that output is connected
        output_component = next((c for c in components if c.component_type == "output"), None)
        if output_component:
            has_incoming = any(c.target_component_id == output_component.id for c in connections)
            if not has_incoming:
                return False, "Output component must have incoming connections"
        
        return True, None
    
    def build_execution_graph(self, workflow: Workflow) -> Dict[int, List[int]]:
        """
        Build execution graph from workflow
        
        Args:
            workflow: Workflow to build graph for
            
        Returns:
            Dictionary mapping component_id to list of target component_ids
        """
        graph = {}
        components = {c.id: c for c in workflow.components}
        connections = workflow.connections
        
        for component_id in components.keys():
            graph[component_id] = []
        
        for conn in connections:
            if conn.source_component_id in graph:
                graph[conn.source_component_id].append(conn.target_component_id)
        
        return graph
    
    def execute_component(
        self,
        component: WorkflowComponent,
        input_data: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """
        Execute a single component
        
        Args:
            component: Component to execute
            input_data: Input data for the component
            db: Database session
            
        Returns:
            Output data from the component
        """
        config = component.config or {}
        component_type = component.component_type
        
        if component_type == "user_query":
            # User query component just passes the query forward
            return {
                "query": input_data.get("query", ""),
                "type": "query"
            }
        
        elif component_type == "knowledgebase":
            # Knowledgebase component retrieves relevant context
            query = input_data.get("query", "")
            knowledgebase_id = component.node_id
            
            # Generate query embedding
            embedding_provider = config.get("embedding_provider", "openai")
            query_embeddings = self.embedding_service.generate_embeddings(
                [query],
                provider=embedding_provider
            )
            
            # Search vector store
            collection_name = config.get("collection_name", "documents")
            n_results = config.get("n_results", 5)
            
            search_results = self.vector_store.search(
                collection_name=collection_name,
                knowledgebase_id=knowledgebase_id,
                query_embedding=query_embeddings[0],
                n_results=n_results
            )
            
            # Combine retrieved documents as context
            context = "\n\n".join(search_results["documents"])
            
            return {
                "query": query,
                "context": context,
                "type": "knowledgebase"
            }
        
        elif component_type == "llm_engine":
            # LLM engine component generates response
            query = input_data.get("query", "")
            context = input_data.get("context")
            
            provider = config.get("provider", "openai")
            model = config.get("model")
            system_prompt = config.get("system_prompt")
            use_web_search = config.get("use_web_search", False)
            temperature = config.get("temperature", 0.7)
            max_tokens = config.get("max_tokens", 1000)
            
            response = self.llm_service.generate_response(
                query=query,
                provider=provider,
                context=context,
                system_prompt=system_prompt,
                use_web_search=use_web_search,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "response": response,
                "type": "llm"
            }
        
        elif component_type == "output":
            # Output component returns the final response
            return {
                "response": input_data.get("response", ""),
                "type": "output"
            }
        
        else:
            raise ValueError(f"Unknown component type: {component_type}")
    
    def execute_workflow(
        self,
        workflow: Workflow,
        query: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Execute a workflow with a query
        
        Args:
            workflow: Workflow to execute
            query: User query
            db: Database session
            
        Returns:
            Execution result
        """
        # Validate workflow
        is_valid, error = self.validate_workflow(workflow)
        if not is_valid:
            return {
                "success": False,
                "error": error,
                "response": None
            }
        
        # Build execution graph
        graph = self.build_execution_graph(workflow)
        components = {c.id: c for c in workflow.components}
        
        # Find user_query component
        user_query_component = next(
            (c for c in workflow.components if c.component_type == "user_query"),
            None
        )
        
        if not user_query_component:
            return {
                "success": False,
                "error": "User Query component not found",
                "response": None
            }
        
        # Execute workflow using BFS
        from collections import deque
        
        queue = deque([(user_query_component.id, {"query": query})])
        visited = set()
        results = {}
        
        while queue:
            component_id, input_data = queue.popleft()
            
            if component_id in visited:
                continue
            
            visited.add(component_id)
            component = components[component_id]
            
            # Execute component
            try:
                output_data = self.execute_component(component, input_data, db)
                results[component_id] = output_data
                
                # Add target components to queue
                for target_id in graph[component_id]:
                    if target_id not in visited:
                        queue.append((target_id, output_data))
            
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Error executing component {component.component_type}: {str(e)}",
                    "response": None
                }
        
        # Find output component result
        output_component = next(
            (c for c in workflow.components if c.component_type == "output"),
            None
        )
        
        if output_component and output_component.id in results:
            final_response = results[output_component.id].get("response", "")
            return {
                "success": True,
                "error": None,
                "response": final_response,
                "metadata": {
                    "components_executed": len(visited),
                    "execution_path": list(visited)
                }
            }
        else:
            return {
                "success": False,
                "error": "Output component did not produce a result",
                "response": None
            }

