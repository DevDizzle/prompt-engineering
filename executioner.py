#!/usr/bin/env python3
"""
executioner.py
--------------
1) Reads artifacts/best_prompt.json to load the 'ultimate_prompt'.
2) Submits that prompt to Gemini 1.5 Pro to produce a final Requirements Analysis.
3) Saves the generated RA to artifacts/Requirements_Analysis.md.
4) Appends the new output (prompt_type="ultimate") to artifacts/experiment_results.csv.
"""

import os
import time
import pandas as pd
import json
import traceback
import google.generativeai as genai

def main():
    # Ensure artifacts directory exists
    artifacts_dir = "artifacts"
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)

    # Define paths to required files
    best_prompt_file = os.path.join(artifacts_dir, "best_prompt.json")
    csv_file_path = os.path.join(artifacts_dir, "experiment_results.csv")
    markdown_file_path = os.path.join(artifacts_dir, "requirements_analysis.md")

    # Debugging: Confirm paths before execution
    print(f"🔍 Checking required files:")
    print(f"   - JSON Input: {best_prompt_file}")
    print(f"   - CSV Output: {csv_file_path}")
    print(f"   - Markdown Output: {markdown_file_path}")

    # 1) Load 'ultimate_prompt' from best_prompt.json
    best_prompt_data = read_best_prompt(best_prompt_file)
    ultimate_prompt = best_prompt_data.get("ultimate_prompt", "").strip()
    
    if not ultimate_prompt:
        raise ValueError("❌ ERROR: 'ultimate_prompt' is missing or empty in best_prompt.json.")

    # 2) Configure Gemini 1.5 Pro
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ ERROR: GEMINI_API_KEY not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

    # 3) Define LLM generation parameters
    final_temperature = 0.3
    final_max_tokens = 2048  # Increased token limit for full analysis

    print(f"🚀 Executing the ultimate prompt with temp={final_temperature}, max_tokens={final_max_tokens}...\n")
    response_text = call_llm(
        model=model,
        prompt_text=ultimate_prompt,
        temperature=final_temperature,
        max_tokens=final_max_tokens
    )

    # 4) Save the Requirements Analysis as Markdown
    save_markdown(markdown_file_path, response_text)

    # 5) Append a new row to experiment_results.csv with 'prompt_type="ultimate"'
    df = load_or_create_csv(csv_file_path)
    new_row = pd.DataFrame([{
        "Prompt Type": "ultimate",
        "Actual Prompt": ultimate_prompt,
        "Temperature": final_temperature,
        "Max Tokens": final_max_tokens,
        "Response Text": response_text
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(csv_file_path, index=False)

    print(f"\n✅ executioner.py: Added 'ultimate' result to {csv_file_path}.\n")
    print(f"📄 Requirements Analysis saved to: {markdown_file_path}\n")
    print(f"Final Requirements Analysis (first 500 chars):\n{response_text[:500]}...\n")

    # Verify CSV file exists after writing
    if os.path.isfile(csv_file_path):
        print(f"✅ Verified: {csv_file_path} exists.")
    else:
        print(f"❌ ERROR: CSV file missing after writing. Check executioner.py.")

def read_best_prompt(filepath):
    """
    Loads best_prompt.json and ensures it contains valid JSON.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"❌ ERROR: File not found: {filepath}")

    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            if not content:  # Handle empty file case
                raise ValueError("❌ ERROR: best_prompt.json is empty or invalid.")
            return json.loads(content)  # Parse JSON

    except json.JSONDecodeError:
        raise ValueError("❌ ERROR: Could not parse JSON from best_prompt.json.")

def load_or_create_csv(csv_file_path):
    """
    Loads experiment_results.csv if it exists, otherwise creates a new empty DataFrame.
    """
    if os.path.isfile(csv_file_path):
        return pd.read_csv(csv_file_path)
    else:
        print(f"⚠️ WARNING: No existing CSV found. Creating a new file at {csv_file_path}.")
        columns = ["Prompt Type", "Actual Prompt", "Temperature", "Max Tokens", "Response Text"]
        return pd.DataFrame(columns=columns)

def call_llm(model, prompt_text, temperature, max_tokens):
    """
    Calls Gemini 1.5 Pro with the final 'ultimate' prompt and returns the RA text.
    """
    try:
        response = model.generate_content(
            prompt_text,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )

        # Debugging: Print a sample of the response
        if response.text:
            print(f"✅ LLM Response (First 200 chars): {response.text.strip()[:200]}...")

        return response.text.strip() if response.text else "No Response"

    except Exception as e:
        print(f"❌ ERROR: LLM call failed: {e}")
        print(traceback.format_exc())  # Print full stack trace
        return f"Error: {e}"

def save_markdown(filepath, content):
    """
    Saves the final Requirements Analysis as a Markdown file.
    """
    markdown_content = f"""# Requirements Analysis Document: ProfitScout Application

{content}

---
*Generated automatically using Gemini 1.5 Pro*
"""

    with open(filepath, "w") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    main()
