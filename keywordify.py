#!/usr/bin/env python3
"""
Keywordify - Extract contextual keywords and generate annotated PDFs

Usage:
    python keywordify.py input.docx [--output-dir ./output] [--api-key YOUR_KEY]
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from docx_reader import DocxReader
from keyword_extractor import KeywordExtractor
from pdf_generator import AnnotatedPDFGenerator
from keyword_list import KeywordListGenerator


class Keywordify:
    """Main orchestrator for keyword extraction and PDF generation."""
    
    def __init__(self, api_key: str = None):
        """Initialize with optional API key."""
        load_dotenv()  # Load from .env file
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY required. Set via --api-key, .env file, or environment variable"
            )
    
    def process(self, input_docx: str, output_dir: str = './output'):
        """
        Process a DOCX file and generate annotated PDFs.
        
        Args:
            input_docx: Path to input DOCX file
            output_dir: Directory for output files
        """
        # Validate input
        if not os.path.exists(input_docx):
            raise FileNotFoundError(f"Input file not found: {input_docx}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate output filenames
        base_name = Path(input_docx).stem
        annotated_pdf = os.path.join(output_dir, f"{base_name}_annotated.pdf")
        keyword_list_pdf = os.path.join(output_dir, f"{base_name}_keywords.pdf")
        
        print(f"Processing: {input_docx}")
        print("-" * 60)
        
        # Step 1: Extract text from DOCX
        print("Step 1: Extracting text from DOCX...")
        reader = DocxReader()
        text = reader.read_text(input_docx)
        para_count = reader.get_paragraph_count(input_docx)
        print(f"  ✓ Extracted {len(text)} characters from {para_count} paragraphs")
        
        # Step 2: Extract keywords using GPT
        print("\nStep 2: Extracting keywords with GPT...")
        extractor = KeywordExtractor(api_key=self.api_key)
        keywords = extractor.extract_keywords(text, min_keywords=3, max_keywords=5)
        print(f"  ✓ Extracted {len(keywords)} keywords:")
        for i, kw in enumerate(keywords, 1):
            print(f"    {i}. {kw}")
        
        # Step 3: Generate annotated PDF
        print("\nStep 3: Generating annotated PDF...")
        pdf_gen = AnnotatedPDFGenerator(annotated_pdf)
        pdf_gen.generate(text, keywords)
        print(f"  ✓ Created: {annotated_pdf}")
        
        # Step 4: Generate keyword list PDF
        print("\nStep 4: Generating keyword list PDF...")
        list_gen = KeywordListGenerator(keyword_list_pdf)
        list_gen.generate(keywords)
        print(f"  ✓ Created: {keyword_list_pdf}")
        
        print("\n" + "=" * 60)
        print("✓ Processing complete!")
        print(f"  • Annotated PDF: {annotated_pdf}")
        print(f"  • Keyword List:  {keyword_list_pdf}")
        print("=" * 60)
        
        return annotated_pdf, keyword_list_pdf


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Extract contextual keywords and generate annotated PDFs',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'input_docx',
        help='Path to input DOCX file'
    )
    
    parser.add_argument(
        '--output-dir',
        default='./output',
        help='Output directory (default: ./output)'
    )
    
    parser.add_argument(
        '--api-key',
        help='OpenAI API key (or set OPENAI_API_KEY env var)'
    )
    
    args = parser.parse_args()
    
    try:
        keywordify = Keywordify(api_key=args.api_key)
        keywordify.process(args.input_docx, args.output_dir)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()