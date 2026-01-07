"""
Text extraction service for documents
"""
import fitz  # PyMuPDF
import os
from typing import Optional
from app.core.config import settings


class TextExtractor:
    """Service for extracting text from documents"""
    
    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            doc = fitz.open(file_path)
            text_content = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    text_content.append(f"--- Page {page_num + 1} ---\n{text}\n")
            
            doc.close()
            return "\n".join(text_content)
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        """
        Extract text from file based on file type
        
        Args:
            file_path: Path to the file
            file_type: MIME type or file extension
            
        Returns:
            Extracted text content
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Normalize file type
        file_type_lower = file_type.lower()
        
        if "pdf" in file_type_lower or file_path.lower().endswith(".pdf"):
            return TextExtractor.extract_from_pdf(file_path)
        else:
            # For other file types, try to read as text
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except UnicodeDecodeError:
                raise ValueError(f"Unsupported file type: {file_type}")
            except Exception as e:
                raise Exception(f"Error reading file: {str(e)}")

