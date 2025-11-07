# Figma Test Generator (Streamlit)

This small project provides a Streamlit UI to upload a Figma screen (image), provide a prompt, and generate automated test scripts (Playwright or Selenium) using an OpenAI model.

## What it does
- UI: Choose source (Figma or Playwright), select target framework (Playwright or Selenium), pick a page header, upload a Figma screen image, and enter additional prompt text.
- Backend: Sends the prompt (and a base64 prefix of the image) to OpenAI to generate a test script.
- Saves the generated file and provides a download button.

## Requirements
- Python 3.8+
- Set environment variable `OPENAI_API_KEY` with your OpenAI API key.

Install deps:

```powershell
python -m pip install -r requirements.txt
```

Run the app:

```powershell
cd figma_test_generator
streamlit run app.py
```

## Notes & Limitations
- The app attaches a truncated base64 prefix of the uploaded image to keep prompts smaller. Very large images can exceed model input limits — compress images before upload if needed.
- You are responsible for providing a valid OpenAI key. The sample uses `gpt-4` in the utils; you can change the model in `utils.py` if needed.
- Generated code should be reviewed and adapted for your test environment (browsers, fixtures, credentials).

## Next steps / Improvements
- Use a vision-enabled model or an image-handling pipeline (OCR, visual parser) for richer UI analysis.
- Add unit tests and CI, and integrate a small caching layer to store previous outputs.
