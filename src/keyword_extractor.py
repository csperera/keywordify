"""
Keyword extraction using OpenAI's GPT API for context-aware keyword selection.
"""

from openai import OpenAI
import os
from typing import List


class KeywordExtractor:
    """Extract contextually relevant keywords from text using GPT."""
    
    def __init__(self, api_key: str = None):
        """Initialize with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment or constructor")
        self.client = OpenAI(api_key=self.api_key)
    
    def extract_keywords(self, text: str, min_keywords: int = 3, max_keywords: int = 5) -> List[str]:
        """
        Extract contextually relevant keywords from text.
        
        Args:
            text: Full document text
            min_keywords: Minimum number of keywords to extract
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            List of keywords in order they should appear in document
        """
        prompt = f"""Analyze this document and extract {min_keywords}-{max_keywords} keywords that:
1. Represent the most important concepts or topics
2. Are contextually significant (not just frequent words)
3. Would help someone quickly understand the document's key themes
4. Are unique and non-overlapping

IMPORTANT: Return ONLY the keywords as a comma-separated list, nothing else.
Example format: keyword1, keyword2, keyword3

Document:
{text}

Keywords:"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4o-mini for cost efficiency
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key concepts from documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        # Extract keywords from response
        response_text = response.choices[0].message.content.strip()
        keywords = [kw.strip() for kw in response_text.split(',')]
        
        # Ensure we have the right number
        keywords = keywords[:max_keywords]
        if len(keywords) < min_keywords:
            raise ValueError(f"Expected at least {min_keywords} keywords, got {len(keywords)}")
            
        return keywords