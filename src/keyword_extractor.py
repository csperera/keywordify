"""
Keyword extraction using OpenAI's GPT API for context-aware keyword selection.
"""

from openai import OpenAI
import os
from typing import List, Optional


class KeywordExtractor:
    """Extract contextually relevant keywords from text using GPT."""
    
    def __init__(self, api_key: str = None):
        """Initialize with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment or constructor")
        self.client = OpenAI(api_key=self.api_key)
    
    def extract_keywords(
        self, 
        text: str, 
        min_keywords: int = 3, 
        max_keywords: int = 5,
        exclude_keywords: Optional[List[str]] = None
    ) -> List[str]:
        """
        Extract contextually relevant keywords from text.
        
        Args:
            text: Full document text
            min_keywords: Minimum number of keywords to extract
            max_keywords: Maximum number of keywords to extract
            exclude_keywords: List of keywords to NOT include (already used)
            
        Returns:
            List of keywords in order they should appear in document
        """
        # Build exclusion instruction if there are keywords to exclude
        exclusion_text = ""
        if exclude_keywords:
            exclusion_text = f"""
IMPORTANT: Do NOT return any of these previously-used keywords (or close variations):
{', '.join(exclude_keywords)}

"""
        
        prompt = f"""Analyze this text and extract the key concepts/keywords.

GUIDELINES:
1. Extract ONLY genuinely important concepts - do NOT pad to reach a number
2. If there are only 2-3 distinct concepts, return only 2-3 keywords
3. Maximum {max_keywords} keywords, but fewer is fine if the content doesn't warrant more
4. Keywords should be contextually significant (not just frequent words)
5. Each keyword should represent a unique concept - no overlapping meanings
{exclusion_text}
IMPORTANT: Return ONLY the keywords as a comma-separated list, nothing else.
If the text has very few concepts, return fewer keywords. Quality over quantity.

Text:
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
        
        # Filter out any excluded keywords that might have slipped through
        if exclude_keywords:
            exclude_lower = {kw.lower() for kw in exclude_keywords}
            keywords = [kw for kw in keywords if kw.lower() not in exclude_lower]
        
        # Ensure we have the right number
        keywords = keywords[:max_keywords]
        if len(keywords) < min_keywords:
            # Don't raise error - just return what we have (later pages may have fewer unique keywords)
            pass
            
        return keywords