# Quick Start Guide

Get up and running with Keywordify in 2 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Your API Key

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

Get your API key at: https://console.anthropic.com/

## Step 3: Create a Sample Document

```bash
python create_sample.py
```

This creates `examples/sample_lecture_notes.docx` with ML content.

## Step 4: Process the Document

```bash
python keywordify.py examples/sample_lecture_notes.docx
```

## Step 5: Check Your Results

Look in the `output/` directory:
- `sample_lecture_notes_annotated.pdf` - Full document with keywords in margins
- `sample_lecture_notes_keywords.pdf` - 3-column keyword list

## That's It! 🎉

Now try it with your own DOCX files:
```bash
python keywordify.py your_lecture_notes.docx
```

## Troubleshooting

**API Key Error?**
- Make sure `.env` file exists with valid `ANTHROPIC_API_KEY`
- Or use: `python keywordify.py input.docx --api-key YOUR_KEY`

**No Keywords Found?**
- Check that your DOCX has actual text content
- Verify the file isn't corrupted

**PDF Looks Weird?**
- Adjust margins in `src/pdf_generator.py`
- Try with different content

## Next Steps

- Read the full [README.md](README.md) for advanced usage
- Customize keyword extraction parameters
- Modify PDF styling and layout
- Process your own lecture notes!
