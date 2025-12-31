"""
PDF generation with keyword highlighting and margin annotations.
Supports per-page keyword extraction for better coverage.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from typing import List, Dict, Optional
import re


class AnnotatedPDFGenerator:
    """Generate PDF with keyword highlighting and margin annotations."""
    
    # Page dimensions
    PAGE_WIDTH, PAGE_HEIGHT = letter
    LEFT_MARGIN = 0.75 * inch
    RIGHT_MARGIN = 0.75 * inch
    TOP_MARGIN = 0.75 * inch
    BOTTOM_MARGIN = 0.75 * inch
    MARGIN_ANNOTATION_WIDTH = 1.5 * inch
    
    # Colors
    HIGHLIGHT_COLOR = HexColor('#FFFF00')  # Yellow
    KEYWORD_TEXT_COLOR = HexColor('#0066CC')  # Blue
    
    def __init__(self, output_path: str, keyword_extractor=None):
        """
        Initialize PDF generator.
        
        Args:
            output_path: Path for output PDF
            keyword_extractor: Optional KeywordExtractor instance for per-page extraction
        """
        self.output_path = output_path
        self.keyword_extractor = keyword_extractor
        self.styles = getSampleStyleSheet()
        
        # Custom style for body text
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_LEFT
        )
        
        # Custom style for margin annotations
        self.margin_style = ParagraphStyle(
            'MarginNote',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            textColor=self.KEYWORD_TEXT_COLOR,
            alignment=TA_LEFT
        )
        
        # Calculate content dimensions
        self.content_x = self.LEFT_MARGIN + self.MARGIN_ANNOTATION_WIDTH + 0.25 * inch
        self.content_width = self.PAGE_WIDTH - self.content_x - self.RIGHT_MARGIN
        self.content_height = self.PAGE_HEIGHT - self.TOP_MARGIN - self.BOTTOM_MARGIN

    def _highlight_paragraph(self, para_text: str, keywords: List[str]) -> str:
        """Add HTML highlighting for keywords in paragraph text."""
        para_html = para_text
        para_lower = para_text.lower()
        
        for keyword in keywords:
            if keyword.lower() in para_lower:
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                match = pattern.search(para_html)
                if match:
                    actual_text = match.group()
                    para_html = para_html.replace(
                        actual_text,
                        f'<b><font color="blue">{actual_text}</font></b>',
                        1  # Only first occurrence per paragraph
                    )
        return para_html

    def _layout_paragraphs(self, paragraphs: List[str]) -> List[List[str]]:
        """
        First pass: Determine which paragraphs fit on each page.
        
        Returns:
            List of pages, where each page is a list of paragraph texts
        """
        pages = []
        current_page = []
        y_position = self.PAGE_HEIGHT - self.TOP_MARGIN
        
        for para_text in paragraphs:
            if not para_text.strip():
                continue
            
            # Create paragraph to measure height
            para = Paragraph(para_text, self.body_style)
            para_width, para_height = para.wrap(self.content_width, self.content_height)
            
            # Check if we need a new page
            if y_position - para_height < self.BOTTOM_MARGIN:
                if current_page:  # Save current page if not empty
                    pages.append(current_page)
                current_page = []
                y_position = self.PAGE_HEIGHT - self.TOP_MARGIN
            
            current_page.append(para_text)
            y_position -= (para_height + 0.15 * inch)
        
        # Don't forget the last page
        if current_page:
            pages.append(current_page)
        
        return pages

    def _extract_keywords_for_page(self, page_paragraphs: List[str], page_num: int) -> List[str]:
        """Extract keywords for a single page's content."""
        if not self.keyword_extractor:
            return []
        
        page_text = '\n\n'.join(page_paragraphs)
        
        # Limit text to avoid token limits (roughly 4 chars per token)
        max_chars = 12000  # ~3000 tokens
        if len(page_text) > max_chars:
            page_text = page_text[:max_chars]
        
        try:
            keywords = self.keyword_extractor.extract_keywords(
                page_text, 
                min_keywords=5, 
                max_keywords=10
            )
            print(f"    Page {page_num}: extracted {len(keywords)} keywords")
            return keywords
        except Exception as e:
            print(f"    Page {page_num}: keyword extraction failed - {e}")
            return []

    def generate(self, text: str, keywords: Optional[List[str]] = None):
        """
        Generate annotated PDF with keywords in margin.
        
        Uses two-pass rendering:
        1. Layout pass - determine page breaks
        2. Render pass - extract keywords per page and render with highlighting
        
        Args:
            text: Full document text
            keywords: Optional pre-extracted keywords (used if no keyword_extractor)
        """
        # Split into paragraphs
        paragraphs = text.split('\n\n')
        
        # Pass 1: Layout to determine pages
        pages = self._layout_paragraphs(paragraphs)
        print(f"  Layout complete: {len(pages)} pages")
        
        # Create canvas for actual rendering
        c = canvas.Canvas(self.output_path, pagesize=letter)
        
        # Collect all keywords across all pages in order of first appearance
        all_keywords = []
        
        # Pass 2: Render each page with its keywords
        for page_num, page_paragraphs in enumerate(pages, 1):
            # Extract keywords for this page
            if self.keyword_extractor:
                page_keywords = self._extract_keywords_for_page(page_paragraphs, page_num)
            else:
                page_keywords = keywords or []
            
            # Add new keywords to list (preserving order of first appearance)
            for kw in page_keywords:
                if kw not in all_keywords:
                    all_keywords.append(kw)
            
            # Track which keywords have been shown in margin for this page
            margin_keywords_shown = set()
            
            y_position = self.PAGE_HEIGHT - self.TOP_MARGIN
            
            for para_text in page_paragraphs:
                if not para_text.strip():
                    continue
                
                para_lower = para_text.lower()
                
                # Find keyword to show in margin (first one in this paragraph not yet shown)
                margin_keyword = None
                for kw in page_keywords:
                    if kw.lower() in para_lower and kw not in margin_keywords_shown:
                        margin_keyword = kw
                        margin_keywords_shown.add(kw)
                        break
                
                # Highlight all keywords in this paragraph
                para_html = self._highlight_paragraph(para_text, page_keywords)
                
                # Create and measure paragraph
                para = Paragraph(para_html, self.body_style)
                para_width, para_height = para.wrap(self.content_width, self.content_height)
                
                # Draw margin annotation if applicable
                if margin_keyword:
                    margin_para = Paragraph(f"<b>{margin_keyword}</b>", self.margin_style)
                    margin_width, margin_height = margin_para.wrap(
                        self.MARGIN_ANNOTATION_WIDTH - 0.2 * inch, 2 * inch
                    )
                    margin_para.drawOn(c, self.LEFT_MARGIN, y_position - margin_height)
                
                # Draw main paragraph
                para.drawOn(c, self.content_x, y_position - para_height)
                
                y_position -= (para_height + 0.15 * inch)
            
            # Start new page (except for last page)
            if page_num < len(pages):
                c.showPage()
        
        c.save()
        print(f"PDF generated: {self.output_path}")
        
        # Return all keywords found (in order of first appearance)
        return all_keywords

