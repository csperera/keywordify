"""
Generate a 3-column keyword list in order of appearance.
Supports multiple pages when there are many keywords.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from typing import List
import math


class KeywordListGenerator:
    """Generate a 3-column keyword list PDF."""
    
    PAGE_WIDTH, PAGE_HEIGHT = letter
    MARGIN = 0.75 * inch
    COLUMN_GAP = 0.5 * inch
    
    def __init__(self, output_path: str):
        """Initialize keyword list generator."""
        self.output_path = output_path
    
    def generate(self, keywords: List[str]):
        """
        Generate 3-column keyword list with multi-page support.
        
        Args:
            keywords: List of keywords in order of appearance
        """
        c = canvas.Canvas(self.output_path, pagesize=letter)
        
        # Calculate column widths
        total_content_width = self.PAGE_WIDTH - (2 * self.MARGIN)
        column_width = (total_content_width - (2 * self.COLUMN_GAP)) / 3
        
        # Column X positions
        col_x = [
            self.MARGIN,
            self.MARGIN + column_width + self.COLUMN_GAP,
            self.MARGIN + (2 * column_width) + (2 * self.COLUMN_GAP)
        ]
        
        # Maximum rows per column (based on page height)
        line_height = 0.25 * inch
        y_start = self.PAGE_HEIGHT - self.MARGIN - 0.5 * inch
        y_end = self.MARGIN
        max_rows_per_column = int((y_start - y_end) / line_height)
        keywords_per_page = max_rows_per_column * 3
        
        # Calculate total pages needed
        total_pages = math.ceil(len(keywords) / keywords_per_page) if keywords else 1
        
        keyword_idx = 0
        
        for page_num in range(1, total_pages + 1):
            # Title with page number
            c.setFont("Helvetica-Bold", 14)
            if total_pages > 1:
                title = f"Keywords (in order of appearance) - Page {page_num} of {total_pages}"
            else:
                title = "Keywords (in order of appearance)"
            c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, title)
            
            # Set font for keywords
            c.setFont("Helvetica", 11)
            
            # Fill columns for this page
            for col in range(3):
                for row in range(max_rows_per_column):
                    if keyword_idx >= len(keywords):
                        break
                    
                    x = col_x[col]
                    y = y_start - (row * line_height)
                    
                    keyword = keywords[keyword_idx]
                    # Truncate long keywords to fit in column
                    display_text = f"• {keyword}"
                    if len(display_text) > 35:
                        display_text = display_text[:32] + "..."
                    
                    c.drawString(x, y, display_text)
                    keyword_idx += 1
                
                if keyword_idx >= len(keywords):
                    break
            
            # Add new page if there are more keywords
            if keyword_idx < len(keywords):
                c.showPage()
        
        c.save()
        print(f"Keyword list generated: {self.output_path}")