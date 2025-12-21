# Keywordify Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Keywordify Workflow                      │
└─────────────────────────────────────────────────────────────┘

   Input: lecture_notes.docx
      │
      ├─► 1. DocxReader
      │      └─► Extract text with paragraph structure
      │
      ├─► 2. KeywordExtractor (Claude API)
      │      ├─► Send full text for contextual analysis
      │      └─► Receive 3-5 contextually relevant keywords
      │
      ├─► 3. AnnotatedPDFGenerator
      │      ├─► Find first occurrence of each keyword
      │      ├─► Highlight keywords in main text (red, bold)
      │      ├─► Place keywords in left margin at first occurrence
      │      └─► Output: lecture_notes_annotated.pdf
      │
      └─► 4. KeywordListGenerator
             ├─► Order keywords by appearance
             ├─► Distribute across 3 columns (top-to-bottom fill)
             └─► Output: lecture_notes_keywords.pdf
```

## Module Responsibilities

### 1. `keywordify.py` (Main Orchestrator)
**Purpose**: CLI interface and workflow coordination

**Responsibilities**:
- Parse command-line arguments
- Validate input files
- Coordinate execution of all modules
- Handle errors and user feedback
- Manage output directory

**Key Methods**:
- `process(input_docx, output_dir)`: Main workflow
- `main()`: CLI entry point

---

### 2. `docx_reader.py` (Document Parser)
**Purpose**: Extract text from DOCX files

**Responsibilities**:
- Read DOCX files using python-docx
- Preserve paragraph structure
- Filter empty paragraphs
- Provide paragraph counts

**Key Methods**:
- `read_text(docx_path)`: Extract all text
- `get_paragraph_count(docx_path)`: Count paragraphs

**Technology**: python-docx library

---

### 3. `keyword_extractor.py` (AI-Powered Extraction)
**Purpose**: Extract contextually relevant keywords using Claude

**Responsibilities**:
- Initialize Anthropic client
- Send text to Claude with extraction prompt
- Parse keyword response
- Validate keyword count (3-5)

**Key Methods**:
- `extract_keywords(text, min_keywords, max_keywords)`: Get keywords

**Technology**: Anthropic Claude Sonnet 4

**Prompt Strategy**:
- Request contextually significant keywords
- Prioritize themes over frequency
- Ensure uniqueness and non-overlap
- Return as comma-separated list

---

### 4. `pdf_generator.py` (Annotated PDF)
**Purpose**: Generate PDF with margin annotations and highlighting

**Responsibilities**:
- Create PDF with custom layout (margin + content)
- Find first occurrence of each keyword
- Highlight keywords in red, bold
- Place keywords in left margin at first occurrence
- Handle pagination

**Key Methods**:
- `generate(text, keywords)`: Create annotated PDF
- `_find_keyword_positions(text, keywords)`: Locate keywords
- `_highlight_text_with_keywords(text, keywords)`: Apply highlighting

**Layout**:
```
┌──────────────────────────────────────────────────────┐
│ [  Margin  ] │ [      Main Content Area      ]       │
│ [  1.5"    ] │ [                             ]       │
│              │                                        │
│ keyword1  ──►│ Text with keyword1 highlighted...     │
│              │                                        │
│              │ More text continues...                │
│              │                                        │
│ keyword2  ──►│ Later text with keyword2 shown...     │
└──────────────────────────────────────────────────────┘
```

**Technology**: ReportLab

---

### 5. `keyword_list.py` (3-Column List)
**Purpose**: Generate ordered keyword list in 3 columns

**Responsibilities**:
- Create PDF with 3-column layout
- Fill columns top-to-bottom, left-to-right
- Maintain order of appearance from main document
- Add bullet points for readability

**Key Methods**:
- `generate(keywords)`: Create keyword list PDF

**Layout Algorithm**:
```python
rows_per_column = ceil(len(keywords) / 3)

for idx, keyword in enumerate(keywords):
    column = idx // rows_per_column
    row = idx % rows_per_column
    # Place at (column_x, row_y)
```

**Technology**: ReportLab

---

## Data Flow

```
DOCX File
   ↓
[DocxReader] → Full Text String
   ↓
[KeywordExtractor] → List[str] of 3-5 Keywords
   ↓                              ↓
   ↓                    [KeywordListGenerator]
   ↓                              ↓
   ↓                    keywords_3col.pdf
   ↓
[AnnotatedPDFGenerator]
   ↓
annotated.pdf
```

## Design Decisions

### 1. **Single Keyword Occurrence**
- **Decision**: Show each keyword only once in margin
- **Rationale**: Cleaner layout, focuses on introduction of concept
- **Implementation**: Track first occurrence position, skip subsequent

### 2. **LLM-Based Extraction**
- **Decision**: Use Claude for keyword extraction
- **Rationale**: 
  - Context-aware (understands semantic importance)
  - Better than statistical methods (TF-IDF, RAKE)
  - Can identify abstract concepts
- **Trade-off**: Requires API call, slower than local methods

### 3. **Red Bold Highlighting**
- **Decision**: Use red + bold for keyword highlights
- **Rationale**: 
  - High visibility
  - Works well in both color and B&W printing
  - Industry standard for emphasis
- **Alternative**: Could use background color (yellow highlighter effect)

### 4. **Left Margin for Annotations**
- **Decision**: 1.5" left margin for keywords
- **Rationale**:
  - Reading flow (left-to-right languages)
  - Avoids interfering with main text
  - Traditional academic annotation style

### 5. **3-Column Sequential Layout**
- **Decision**: Fill columns top-to-bottom, order of appearance
- **Rationale**:
  - Maintains chronological context
  - Natural reading flow
  - Easy to reference back to main document

### 6. **Modular Architecture**
- **Decision**: Separate modules for each responsibility
- **Rationale**:
  - Easy to test individual components
  - Can swap implementations (e.g., different PDF libraries)
  - Clean separation of concerns
  - Extensible for future features

## Extension Points

### Adding New Input Formats
Implement new reader class with same interface:
```python
class PDFReader:
    @staticmethod
    def read_text(pdf_path: str) -> str:
        # Implementation
        pass
```

### Custom Keyword Extraction
Replace `KeywordExtractor` with custom implementation:
```python
class CustomExtractor:
    def extract_keywords(self, text: str, min_keywords: int, 
                        max_keywords: int) -> List[str]:
        # Your algorithm here
        pass
```

### Different PDF Layouts
Subclass `AnnotatedPDFGenerator`:
```python
class RightMarginPDFGenerator(AnnotatedPDFGenerator):
    MARGIN_ANNOTATION_WIDTH = 1.5 * inch  # Right side
    # Override positioning methods
```

## Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| DOCX Reading | O(n) | n = number of paragraphs |
| Keyword Extraction | O(1)* | Fixed API call (*network dependent) |
| PDF Generation | O(n×k) | n = text length, k = keywords |
| Keyword List | O(k) | k = number of keywords (3-5) |

**Overall**: Linear with respect to document size, dominated by API call latency

## Dependencies

```
python-docx (Document parsing)
    ↓
reportlab (PDF generation)
    ↓
anthropic (Keyword extraction)
    ↓
python-dotenv (Environment config)
```

**No circular dependencies** - Clean dependency tree

## Testing Strategy

1. **Unit Tests**: Each module independently
2. **Integration Tests**: Full workflow with sample documents
3. **Edge Cases**: 
   - Very short documents (<100 words)
   - Very long documents (>10,000 words)
   - Documents with no clear keywords
   - Special characters in keywords
   - Multiple occurrences of keywords

## Security Considerations

1. **API Key**: Stored in `.env`, never committed
2. **Input Validation**: Check file exists before processing
3. **Error Handling**: Graceful failures with user feedback
4. **No Code Execution**: Pure data processing, no eval/exec

## Future Enhancements

1. **Batch Processing**: Process multiple files
2. **Keyword Export**: JSON/CSV output
3. **Custom Styling**: User-defined colors, fonts
4. **Multi-Language**: Support for non-English documents
5. **Real-time Preview**: GUI with live updates
6. **Cloud Integration**: Google Drive, Dropbox support
