# Keywordify - OpenAI Setup Instructions

## What Changed

✅ Updated to use **OpenAI GPT-4o-mini** for keyword extraction
✅ More cost-effective than GPT-4
✅ Fast and accurate for this task

## Files Updated

Download and replace these 4 files in your project:

1. **requirements.txt** - Now uses `openai` package
2. **.env.example** - Template for `OPENAI_API_KEY`
3. **keywordify.py** - References OpenAI instead of Anthropic
4. **src/keyword_extractor.py** - Uses OpenAI Chat Completions API

## Installation Steps (PowerShell)

```powershell
cd C:\users\chris\keywordify

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies (now includes openai package)
pip install -r requirements.txt

# Create .env file
copy .env.example .env
```

## Set Your OpenAI API Key

1. Get your API key from: https://platform.openai.com/api-keys
2. Open `.env` in Google Antigravity
3. Replace the line with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```
4. Save the file

## Test It

```powershell
# Create sample document
python create_sample.py

# Run Keywordify
python keywordify.py examples\sample_lecture_notes.docx
```

## Expected Output

```
Processing: examples\sample_lecture_notes.docx
------------------------------------------------------------
Step 1: Extracting text from DOCX...
  ✓ Extracted 2547 characters from 6 paragraphs

Step 2: Extracting keywords with GPT...
  ✓ Extracted 5 keywords:
    1. supervised learning
    2. neural networks
    3. gradient descent
    4. backpropagation
    5. regularization

Step 3: Generating annotated PDF...
  ✓ Created: output\sample_lecture_notes_annotated.pdf

Step 4: Generating keyword list PDF...
  ✓ Created: output\sample_lecture_notes_keywords.pdf

============================================================
✓ Processing complete!
============================================================
```

## Why GPT-4o-mini?

- **Cost-effective**: ~15x cheaper than GPT-4
- **Fast**: Lower latency
- **Accurate**: More than capable for keyword extraction
- **Your existing plan**: Works with your OpenAI subscription

If you want even better results, you can change the model in `src/keyword_extractor.py`:
```python
model="gpt-4o"  # or "gpt-4-turbo"
```

## Troubleshooting

**"OPENAI_API_KEY not found"**
→ Make sure `.env` file exists (not `.env.example`) and contains your key

**"Incorrect API key provided"**
→ Double-check your API key at https://platform.openai.com/api-keys

**"Rate limit exceeded"**
→ Your API key might need billing enabled at https://platform.openai.com/account/billing

## You're All Set! 🚀

Process your 30-page lecture notes:
```powershell
python keywordify.py path\to\your\lecture_notes.docx
```