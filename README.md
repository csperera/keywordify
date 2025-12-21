# Keywordify v1.0

**Contextual keyword extraction and PDF annotation using AI**

Keywordify uses Claude AI to intelligently extract 3-5 contextually significant keywords from lecture notes or documents, then generates two outputs:

1. **Annotated PDF**: Original text with keywords highlighted and annotated in the margin
2. **Keyword List**: 3-column list of keywords in order of appearance

## Features

- ✨ **Context-aware keyword extraction** using Claude's language understanding
- 📝 **Margin annotations** showing keywords at first occurrence
- 🎯 **Smart highlighting** of keywords in main text (red, bold)
- 📊 **3-column keyword list** in sequential order
- 🚀 **Clean modular architecture** for easy extension

## Installation

### Prerequisites
- Python 3.8+
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Setup

```bash
# Clone repository
git clone <your-repo-url>
cd Keywordify

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

## Usage

### Basic Usage

```bash
python keywordify.py input.docx
```

This creates two PDFs in `./output/`:
- `input_annotated.pdf` - Full document with keyword annotations
- `input_keywords.pdf` - 3-column keyword list

### Custom Output Directory

```bash
python keywordify.py lecture_notes.docx --output-dir ./my_outputs
```

### API Key via Command Line

```bash
python keywordify.py input.docx --api-key sk-ant-xxxxx
```

## Example Output

### Input
30 pages of lecture notes on machine learning

### Keywords Extracted (by Claude)
1. supervised learning
2. neural networks
3. gradient descent
4. backpropagation
5. regularization

### Output 1: Annotated PDF
```
[Margin]              [Main Text]
supervised learning → Machine learning algorithms can be categorized into
                     supervised learning and unsupervised learning...
                     
                     In supervised learning, the model is trained on
                     labeled data...

neural networks    → A neural network is composed of layers of 
                     interconnected nodes...
```

### Output 2: Keyword List (3 columns)
```
Column 1              Column 2           Column 3
• supervised learning • backpropagation  
• neural networks     • regularization
• gradient descent    
```

## Architecture

```
Keywordify/
├── keywordify.py          # Main orchestrator script
├── src/
│   ├── docx_reader.py     # Extract text from DOCX files
│   ├── keyword_extractor.py  # Claude-powered keyword extraction
│   ├── pdf_generator.py   # Annotated PDF with margins
│   └── keyword_list.py    # 3-column keyword list generator
├── requirements.txt
├── README.md
└── .env                   # API key (not committed)
```

## Design Decisions

### Keyword Extraction
- Uses Claude Sonnet 4 for contextual understanding
- Extracts 3-5 keywords (configurable)
- Considers semantic importance, not just frequency
- Keywords are unique and non-overlapping

### PDF Generation
- **reportlab** for precise layout control
- Left margin (1.5") reserved for annotations
- Keywords shown only at first occurrence
- Red bold highlighting for easy scanning
- Blue margin text for visual separation

### Keyword Ordering
- Sequential order matches appearance in document
- 3-column layout fills top-to-bottom, then left-to-right
- Maintains reading flow for quick reference

## Configuration

### Adjust Keyword Count

Edit `keywordify.py`:
```python
keywords = extractor.extract_keywords(text, min_keywords=2, max_keywords=7)
```

### Change Highlight Color

Edit `src/pdf_generator.py`:
```python
HIGHLIGHT_COLOR = HexColor('#0011ff8a')  # blue

### Adjust Margins

Edit `src/pdf_generator.py`:
```python
MARGIN_ANNOTATION_WIDTH = 2.0 * inch  # Wider margin
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
- Uses modular design with single-responsibility classes
- Type hints for all public methods
- Docstrings following Google style

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Set your API key in `.env` file or via `--api-key` flag

### "Keyword not found in text"
Some keywords may not match exactly due to capitalization or spacing. The script will warn but continue.

### PDF Layout Issues
Adjust `MARGIN_ANNOTATION_WIDTH` and content margins in `pdf_generator.py`

## Future Enhancements

- [ ] Support for PDF input documents
- [ ] Batch processing multiple files
- [ ] Custom keyword count per document
- [ ] Export keywords to CSV/JSON
- [ ] Different highlighting styles (underline, background color)
- [ ] Support for different page sizes
- [ ] Multi-language support

## License

MIT

## Author

Cristian Perera - AI/ML Engineer specializing in PropTech applications

## Acknowledgments

- PDF generation via [ReportLab](https://www.reportlab.com/)
- Document parsing via [python-docx](https://python-docx.readthedocs.io/)
