"""
LLM service for interacting with language models
"""
from typing import Optional, Dict, Any
import openai
from google.generativeai import configure, GenerativeModel
import serpapi
from app.core.config import settings


class LLMService:
    """Service for interacting with LLMs"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        if settings.GEMINI_API_KEY:
            configure(api_key=settings.GEMINI_API_KEY)
        if settings.SERPAPI_API_KEY:
            self.serpapi_key = settings.SERPAPI_API_KEY
        else:
            self.serpapi_key = None
    
    def generate_openai_response(
        self,
        query: str,
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate response using OpenAI GPT
        
        Args:
            query: User query
            context: Optional context from knowledgebase
            system_prompt: Optional system prompt
            model: OpenAI model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            elif context:
                messages.append({
                    "role": "system",
                    "content": f"You are a helpful assistant. Use the following context to answer questions:\n\n{context}"
                })
            else:
                messages.append({
                    "role": "system",
                    "content": "You are a helpful assistant."
                })
            
            messages.append({"role": "user", "content": query})
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Error generating OpenAI response: {str(e)}")
    
    def generate_gemini_response(
        self,
        query: str,
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: str = "gemini-pro",
        temperature: float = 0.7
    ) -> str:
        """
        Generate response using Google Gemini
        
        Args:
            query: User query
            context: Optional context from knowledgebase
            system_prompt: Optional system prompt
            model: Gemini model name
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        try:
            if not settings.GEMINI_API_KEY:
                raise ValueError("Gemini API key not configured")
            
            # Build prompt
            prompt_parts = []
            
            if system_prompt:
                prompt_parts.append(system_prompt)
            elif context:
                prompt_parts.append(f"Context:\n{context}\n\n")
            
            prompt_parts.append(f"Question: {query}\n\nAnswer:")
            
            full_prompt = "\n".join(prompt_parts)
            
            gemini_model = GenerativeModel(model)
            response = gemini_model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": temperature,
                }
            )
            
            return response.text
        
        except Exception as e:
            raise Exception(f"Error generating Gemini response: {str(e)}")
    
    def search_web(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search the web using SerpAPI
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Dictionary with search results
        """
        if not self.serpapi_key:
            raise ValueError("SerpAPI key not configured")
        
        try:
            search = serpapi.GoogleSearch({
                "q": query,
                "api_key": self.serpapi_key,
                "num": num_results
            })
            
            results = search.get_dict()
            
            # Extract relevant information
            organic_results = results.get("organic_results", [])
            
            return {
                "query": query,
                "results": [
                    {
                        "title": r.get("title", ""),
                        "link": r.get("link", ""),
                        "snippet": r.get("snippet", "")
                    }
                    for r in organic_results[:num_results]
                ]
            }
        
        except Exception as e:
            raise Exception(f"Error searching web: {str(e)}")
    
    def generate_response(
        self,
        query: str,
        provider: str = "openai",
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
        use_web_search: bool = False,
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate response using specified provider
        
        Args:
            query: User query
            provider: LLM provider (openai or gemini)
            context: Optional context from knowledgebase
            system_prompt: Optional system prompt
            use_web_search: Whether to use web search
            model: Model name (optional)
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        # If web search is enabled, add search results to context
        if use_web_search:
            try:
                search_results = self.search_web(query)
                web_context = "\n\nWeb Search Results:\n"
                for i, result in enumerate(search_results["results"], 1):
                    web_context += f"{i}. {result['title']}\n{result['snippet']}\n{result['link']}\n\n"
                
                if context:
                    context = f"{context}\n\n{web_context}"
                else:
                    context = web_context
            except Exception as e:
                # If web search fails, continue without it
                print(f"Web search failed: {str(e)}")
        
        # Generate response
        if provider.lower() == "openai":
            model = model or kwargs.get("model", "gpt-3.5-turbo")
            return self.generate_openai_response(
                query=query,
                context=context,
                system_prompt=system_prompt,
                model=model,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000)
            )
        elif provider.lower() == "gemini":
            model = model or kwargs.get("model", "gemini-pro")
            return self.generate_gemini_response(
                query=query,
                context=context,
                system_prompt=system_prompt,
                model=model,
                temperature=kwargs.get("temperature", 0.7)
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

