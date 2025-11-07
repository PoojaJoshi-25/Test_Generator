import os
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def generate_test_script(prompt: str, image_bytes: bytes, framework: str,
                         page_header: str = None, base_url: str = None, num_tests: int = 1, use_stub: bool = False) -> dict:
    """
    Generate Playwright test automation code in 3 separate files:
    locators.py, actions.py, and test_script.py.
    Optionally injects a Base URL into the test script.
    """

    if not GEMINI_API_KEY:
        return {"error": "❌ GEMINI_API_KEY not set in .env"}

    # --- User Prompt (to Gemini) ---
    user_prompt = f"""
You are an expert Playwright test engineer.

From the provided Figma UI image, generate Python-based Playwright test automation code
in 3 clearly separated sections, each starting with markers:

###LOCATORS###
- Define element locator classes or constants.

###ACTIONS###
- Define action classes that perform operations (click, type, verify, etc.) using locators.
- Use Playwright's sync API.

###TEST###
- Write realistic Playwright test cases that call the above actions.
- Ensure code can run with pytest.
- Use a variable BASE_URL for the website URL instead of hardcoding it.

Use OOP design, meaningful class names, and clean formatting.
"""

    # --- Initialize model ---
    model = genai.GenerativeModel("gemini-2.0-flash")

    # --- Build input parts for Gemini ---
    parts = [{"role": "user", "parts": [{"text": user_prompt}]}]
    if image_bytes:
        parts[0]["parts"].append({
            "inline_data": {"mime_type": "image/png", "data": image_bytes}
        })

    # --- Call Gemini API ---
    try:
        response = model.generate_content(parts)
    except Exception as e:
        return {"error": f"Gemini API call failed: {e}"}

    # --- Validate Response ---
    if not getattr(response, "text", None):
        return {"error": "No response text received from Gemini."}

    full_text = response.text.strip()
    locators, actions, test_script = _split_script_sections(full_text)

    # --- Inject Base URL if provided ---
    if base_url:
        base_url_code = f'BASE_URL = "{base_url.rstrip("/")}"\n\n'
        test_script = base_url_code + test_script.replace(
            'https://example.com', 'BASE_URL'
        )

    # --- Save into playwright_project folder ---
    base_path = "../playwright_project"
    os.makedirs(base_path, exist_ok=True)

    files = {
        "locators.py": locators or "# No locators generated",
        "actions.py": actions or "# No actions generated",
        "test_script.py": test_script or "# No test script generated"
    }

    for fname, content in files.items():
        with open(os.path.join(base_path, fname), "w", encoding="utf-8") as f:
            f.write(content)

    # --- Return summary to app.py ---
    return {
        "script": full_text,
        "filename": "combined_output.txt",
        "files": list(files.keys())
    }


def _split_script_sections(full_text: str):
    """Extract LOCATORS, ACTIONS, and TEST parts from Gemini's response."""
    locators = actions = test_script = ""
    try:
        locators = full_text.split("###LOCATORS###")[1].split("###ACTIONS###")[0].strip()
        actions = full_text.split("###ACTIONS###")[1].split("###TEST###")[0].strip()
        test_script = full_text.split("###TEST###")[1].strip()
    except Exception:
        pass
    return locators, actions, test_script
