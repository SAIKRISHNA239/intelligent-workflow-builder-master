"""
Embedding generation service
"""
from typing import List, Optional
import openai
from google.generativeai import configure, embed_content
from app.core.config import settings


class EmbeddingService:
    """Service for generating embeddings"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        if settings.GEMINI_API_KEY:
            configure(api_key=settings.GEMINI_API_KEY)
    
    def generate_openai_embeddings(self, texts: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
        """
        Generate embeddings using OpenAI
        
        Args:
            texts: List of text strings to embed
            model: OpenAI embedding model name
            
        Returns:
            List of embedding vectors
        """
        try:
            response = openai.embeddings.create(
                model=model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise Exception(f"Error generating OpenAI embeddings: {str(e)}")
    
    def generate_gemini_embeddings(self, texts: List[str], model: str = "models/embedding-001") -> List[List[float]]:
        """
        Generate embeddings using Google Gemini
        
        Args:
            texts: List of text strings to embed
            model: Gemini embedding model name
            
        Returns:
            List of embedding vectors
        """
        try:
            if not settings.GEMINI_API_KEY:
                raise ValueError("Gemini API key not configured")
            
            embeddings = []
            for text in texts:
                result = embed_content(
                    model=model,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result["embedding"])
            
            return embeddings
        except Exception as e:
            raise Exception(f"Error generating Gemini embeddings: {str(e)}")
    
    def generate_embeddings(self, texts: List[str], provider: str = "openai", model: Optional[str] = None) -> List[List[float]]:
        """
        Generate embeddings using specified provider
        
        Args:
            texts: List of text strings to embed
            provider: Embedding provider (openai or gemini)
            model: Model name (optional, uses default if not provided)
            
        Returns:
            List of embedding vectors
        """
        if provider.lower() == "openai":
            model = model or "text-embedding-ada-002"
            return self.generate_openai_embeddings(texts, model)
        elif provider.lower() == "gemini":
            model = model or "models/embedding-001"
            return self.generate_gemini_embeddings(texts, model)
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")

