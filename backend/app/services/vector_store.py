"""
Vector store service using ChromaDB
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Optional, Dict, Any
import uuid
from app.core.config import settings


class VectorStoreService:
    """Service for managing vector store operations"""
    
    def __init__(self):
        """Initialize ChromaDB client"""
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
    
    def create_collection(self, collection_name: str, knowledgebase_id: str) -> chromadb.Collection:
        """
        Create or get a collection for a knowledgebase
        
        Args:
            collection_name: Name of the collection
            knowledgebase_id: Knowledgebase component ID
            
        Returns:
            ChromaDB collection
        """
        # Use knowledgebase_id as part of collection name for uniqueness
        full_name = f"{collection_name}_{knowledgebase_id}"
        
        try:
            collection = self.client.get_collection(name=full_name)
        except:
            collection = self.client.create_collection(
                name=full_name,
                metadata={"knowledgebase_id": knowledgebase_id}
            )
        
        return collection
    
    def add_documents(
        self,
        collection_name: str,
        knowledgebase_id: str,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Add documents to the vector store
        
        Args:
            collection_name: Name of the collection
            knowledgebase_id: Knowledgebase component ID
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadatas: Optional list of metadata dictionaries
            
        Returns:
            List of document IDs
        """
        collection = self.create_collection(collection_name, knowledgebase_id)
        
        # Generate IDs for documents
        ids = [str(uuid.uuid4()) for _ in texts]
        
        # Prepare metadatas
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        # Add to collection
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def search(
        self,
        collection_name: str,
        knowledgebase_id: str,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for similar documents
        
        Args:
            collection_name: Name of the collection
            knowledgebase_id: Knowledgebase component ID
            query_embedding: Query embedding vector
            n_results: Number of results to return
            where: Optional filter metadata
            
        Returns:
            Dictionary with results (ids, documents, distances, metadatas)
        """
        collection = self.create_collection(collection_name, knowledgebase_id)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        return {
            "ids": results["ids"][0] if results["ids"] else [],
            "documents": results["documents"][0] if results["documents"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else []
        }
    
    def delete_collection(self, collection_name: str, knowledgebase_id: str) -> bool:
        """
        Delete a collection
        
        Args:
            collection_name: Name of the collection
            knowledgebase_id: Knowledgebase component ID
            
        Returns:
            True if successful
        """
        try:
            full_name = f"{collection_name}_{knowledgebase_id}"
            self.client.delete_collection(name=full_name)
            return True
        except Exception as e:
            print(f"Error deleting collection: {str(e)}")
            return False

