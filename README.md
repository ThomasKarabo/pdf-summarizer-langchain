# Lecture Notes Summarizer

A small Python project that extracts text from a PDF of lecture notes and uses LangChain + OpenAI to produce a structured summary (introduction, body, conclusion), a study schedule, and revision questions.

## Repository structure

- `main.py` - Example entrypoint that builds a ChatPromptTemplate and runs a chain to summarize lecture notes, create a 7-day reading schedule, and produce revision questions.
- `model.py` - A `TeacherModel` class that wraps prompt creation and a call to `ChatOpenAI` to produce a structured summary for a provided document. This file also demonstrates a direct script-mode run that extracts text and prints the model response.
- `transform.py` - Uses PyMuPDF (`fitz`) to extract plain text from a PDF file.
- `requirements.txt` - Pins the LangChain-related dependencies used by this project.

## Prerequisites

- Python 3.9+ (3.10+ recommended)
- Windows PowerShell (examples below use PowerShell)
- A valid OpenAI API key with access to the model you want to use.
- The PDF file (for example `DSP - Lecture Notes (Chapter 1).pdf`) placed in the project root or an accessible path.

## Setup

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:

```
OPENAI_API_KEY=sk-<your_api_key_here>
```

4. Place the PDF you want to summarize in the project folder (or update the filename used in `main.py` / `model.py`).

## Usage

Two example entrypoints are included. Use whichever matches your desired flow.

- Run the main example (recommended):

```powershell
python main.py
```

This will:
- extract text from the PDF using `transform.extract_text_from_fitz`
- build a prompt asking the model to summarize, create a 7-day reading schedule, and produce revision questions
- print the model output to console

- Run the `TeacherModel` example directly:

```powershell
python model.py
```

This will run the `TeacherModel` flow which:
- loads the PDF text
- sets a system prompt and user prompt (asking for a 3-paragraph summary with introduction/body/conclusion)
- invokes the model and prints the result

## Configuration & Tips

- API key: confirm `OPENAI_API_KEY` is present in your environment or `.env` file. `python-dotenv` is used to load `.env`.
- Model names: The code references model names in `main.py` / `model.py`. If you get an API error, change the model name to a model your account supports (e.g., `gpt-4` or an available gpt-4o variant). Update the `model=` argument in the `ChatOpenAI(...)` constructor.
- Truncation: `model.py` contains a safety truncation that limits `self.document` to 10,000 characters before sending to the prompt. If you need longer context, remove or increase that limit, or split the document and process in chunks.
- Temperature: change the `temperature` parameter to control creativity (0.0 deterministic, up to ~1.0 more creative).

## Troubleshooting

- "No output" or empty summary:
  - Confirm the PDF path is correct and `transform.extract_text_from_fitz` returns non-empty text.
  - Confirm your `OPENAI_API_KEY` is valid and has quota.
  - Check for exceptions printed in the console (extractor or LangChain errors).

- Model/Authorization errors:
  - If you see invalid_model or access errors, change the `model` parameter in `ChatOpenAI(...)` to a supported model. Some accounts do not have access to certain model families.

## Safety & Limits

- This project sends text to OpenAI APIs. Do not include sensitive or private data in the PDF.
- Large PDFs may hit token limits. Consider splitting long documents or summarizing by sections.

## Next steps / Improvements

- Add chunking with `langchain.text_splitters` and summarize/concat to handle long documents robustly.
- Save outputs to a file (e.g., `summary.txt` or `summary.md`) instead of printing to stdout.
- Add unit tests for `transform.extract_text_from_fitz` and the prompt templates.

## License

This repository does not include a license file. Add one if you plan to share or reuse this project publicly.

## Contact / Help

If something doesn't work, share the console output and I can help debug further (missing dependencies, API errors, or PDF parsing issues).