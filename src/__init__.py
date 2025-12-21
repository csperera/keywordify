"""
Keywordify - Contextual keyword extraction and PDF annotation.
"""

__version__ = "1.0.0"
__author__ = "Cristian"

from .docx_reader import DocxReader
from .keyword_extractor import KeywordExtractor
from .pdf_generator import AnnotatedPDFGenerator
from .keyword_list import KeywordListGenerator

__all__ = [
    'DocxReader',
    'KeywordExtractor',
    'AnnotatedPDFGenerator',
    'KeywordListGenerator'
]
