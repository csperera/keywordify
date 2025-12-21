"""
Generate a 3-column keyword list in order of appearance.
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
        Generate 3-column keyword list.
        
        Args:
            keywords: List of keywords in order of appearance
        """
        c = canvas.Canvas(self.output_path, pagesize=letter)
        
        # Calculate column widths
        total_content_width = self.PAGE_WIDTH - (2 * self.MARGIN)
        column_width = (total_content_width - (2 * self.COLUMN_GAP)) / 3
        
        # Column X positions
        col1_x = self.MARGIN
        col2_x = self.MARGIN + column_width + self.COLUMN_GAP
        col3_x = self.MARGIN + (2 * column_width) + (2 * self.COLUMN_GAP)
        
        # Maximum rows per column (based on page height)
        # Conservative estimate: ~30 rows per column
        max_rows_per_column = 30
        
        # Title
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.MARGIN, self.PAGE_HEIGHT - self.MARGIN, "Keywords (in order of appearance)")
        
        # Starting Y position for keywords
        y_start = self.PAGE_HEIGHT - self.MARGIN - 0.5 * inch
        line_height = 0.25 * inch
        
        c.setFont("Helvetica", 11)
        
        # Fill columns sequentially: fill column 1 completely, then column 2, then column 3
        for idx, keyword in enumerate(keywords):
            # Determine which column this keyword goes in
            if idx < max_rows_per_column:
                # Column 1
                x = col1_x
                row = idx
            elif idx < 2 * max_rows_per_column:
                # Column 2
                x = col2_x
                row = idx - max_rows_per_column
            else:
                # Column 3
                x = col3_x
                row = idx - (2 * max_rows_per_column)
            
            y = y_start - (row * line_height)
            
            # Draw keyword with bullet
            c.drawString(x, y, f"• {keyword}")
        
        c.save()
        print(f"Keyword list generated: {self.output_path}")