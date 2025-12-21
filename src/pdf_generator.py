"""
PDF generation with keyword highlighting and margin annotations.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_LEFT
from typing import List, Tuple, Dict
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
    MARGIN_TEXT_COLOR = HexColor('#0066CC')  # Blue
    
    def __init__(self, output_path: str):
        """Initialize PDF generator."""
        self.output_path = output_path
        self.c = canvas.Canvas(output_path, pagesize=letter)
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
            textColor=self.MARGIN_TEXT_COLOR,
            alignment=TA_LEFT
        )
    
    def _find_keyword_positions(self, text: str, keywords: List[str]) -> Dict[str, int]:
        """
        Find first occurrence position of each keyword in text.
        
        Returns:
            Dict mapping keyword to character position of first occurrence
        """
        positions = {}
        text_lower = text.lower()
        
        for keyword in keywords:
            # Find first occurrence (case-insensitive)
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            match = pattern.search(text)
            if match:
                positions[keyword] = match.start()
            else:
                # If exact match not found, skip this keyword
                print(f"Warning: Keyword '{keyword}' not found in text")
        
        return positions
    
    def _highlight_text_with_keywords(self, text: str, keywords: List[str]) -> Tuple[str, List[int]]:
        """
        Add HTML highlighting to first occurrence of each keyword.
        
        Returns:
            Tuple of (highlighted_html, list of character positions where keywords occur)
        """
        positions = self._find_keyword_positions(text, keywords)
        
        # Sort keywords by position (earliest first)
        sorted_keywords = sorted(positions.items(), key=lambda x: x[1])
        
        # Build highlighted text by replacing from end to start (to preserve positions)
        result = text
        keyword_positions = []
        
        for keyword, pos in reversed(sorted_keywords):
            # Find the actual text (preserving case)
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            match = pattern.search(result[pos:pos+len(keyword)+10])
            if match:
                actual_text = match.group()
                highlighted = f'<b><font color="red">{actual_text}</font></b>'
                result = result[:pos] + highlighted + result[pos+len(actual_text):]
                keyword_positions.append(pos)
        
        return result, sorted([kw for kw, _ in sorted_keywords])
    
    def generate(self, text: str, keywords: List[str]):
        """
        Generate annotated PDF with keywords in margin.
        
        Args:
            text: Full document text
            keywords: List of keywords to annotate
        """
        # Prepare text with highlighting
        highlighted_html, ordered_keywords = self._highlight_text_with_keywords(text, keywords)
        
        # Split into paragraphs
        paragraphs = text.split('\n\n')
        
        # Calculate content area
        content_x = self.LEFT_MARGIN + self.MARGIN_ANNOTATION_WIDTH + 0.25 * inch
        content_width = self.PAGE_WIDTH - content_x - self.RIGHT_MARGIN
        content_height = self.PAGE_HEIGHT - self.TOP_MARGIN - self.BOTTOM_MARGIN
        
        y_position = self.PAGE_HEIGHT - self.TOP_MARGIN
        current_keyword_idx = 0
        
        for para_text in paragraphs:
            if not para_text.strip():
                continue
            
            # Check if this paragraph contains any un-annotated keywords
            para_lower = para_text.lower()
            margin_keyword = None
            
            if current_keyword_idx < len(ordered_keywords):
                keyword = ordered_keywords[current_keyword_idx]
                if keyword.lower() in para_lower:
                    margin_keyword = keyword
                    current_keyword_idx += 1
            
            # Highlight keywords in this paragraph
            para_html = para_text
            for keyword in ordered_keywords:
                if keyword.lower() in para_lower:
                    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                    match = pattern.search(para_html)
                    if match:
                        actual_text = match.group()
                        para_html = para_html.replace(
                            actual_text,
                            f'<b><font color="red">{actual_text}</font></b>',
                            1  # Only first occurrence
                        )
            
            # Create paragraph object
            para = Paragraph(para_html, self.body_style)
            para_width, para_height = para.wrap(content_width, content_height)
            
            # Check if we need a new page
            if y_position - para_height < self.BOTTOM_MARGIN:
                self.c.showPage()
                y_position = self.PAGE_HEIGHT - self.TOP_MARGIN
            
            # Draw margin annotation if this paragraph has a keyword
            if margin_keyword:
                margin_para = Paragraph(f"<b>{margin_keyword}</b>", self.margin_style)
                margin_width, margin_height = margin_para.wrap(self.MARGIN_ANNOTATION_WIDTH - 0.2 * inch, 2 * inch)
                
                # Draw in margin
                margin_para.drawOn(
                    self.c,
                    self.LEFT_MARGIN,
                    y_position - margin_height
                )
            
            # Draw main paragraph
            para.drawOn(self.c, content_x, y_position - para_height)
            
            # Update position
            y_position -= (para_height + 0.15 * inch)
        
        self.c.save()
        print(f"PDF generated: {self.output_path}")
