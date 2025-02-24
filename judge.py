#!/usr/bin/env python3
"""
judge.py
--------------
import os
import json
import pandas as pd
import traceback
import re
import google.generativeai as genai

def main():
    print("🔍 Debug: Starting judge.py")

    # Ensure artifacts directory exists
    artifacts_dir = "artifacts"
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)
    print(f"✅ Debug: Artifacts directory checked at '{artifacts_dir}'")

    # Define correct paths
    csv_file_path = os.path.join(artifacts_dir, "experiment_results.csv")
    best_prompt_file = os.path.join(artifacts_dir, "best_prompt.json")
    markdown_file_path = os.path.join(artifacts_dir, "best_prompt_reasoning.md")

    print(f"🔍 Debug: Looking for CSV at '{csv_file_path}'")
    if not os.path.isfile(csv_file_path):
        print(f"❌ ERROR: '{csv_file_path}' not found. Run generator.py first.")
        return

    print("✅ Debug: CSV file found. Reading contents...")
    df = pd.read_csv(csv_file_path)
    print("✅ Debug: CSV loaded successfully")
    experiment_data = df.to_dict(orient="records")

    # Configure Gemini 1.5 Pro
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not set.")
        return

    print("✅ Debug: GEMINI_API_KEY detected, configuring API...")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")
    print("✅ Debug: Gemini model configured")

    # Step 1: Identify the Best Prompt
    print("🔍 Debug: Asking LLM to select the best prompt based on outputs...")
    selection_prompt = build_judge_prompt(experiment_data)
    raw_judge_response = call_llm(model, selection_prompt)
    best_prompt_data = parse_judge_json(raw_judge_response)

    # Step 2: Refine the Best Prompt
    print("🔍 Debug: Asking LLM to refine the best prompt if needed...")
    refined_prompt = refine_best_prompt(model, best_prompt_data)
    best_prompt_data["ultimate_prompt"] = refined_prompt

    # Step 3: Save best prompt & reasoning
    save_json(best_prompt_file, best_prompt_data)
    save_markdown(markdown_file_path, best_prompt_data)

    print("✅ judge.py: Successfully completed!")

def build_judge_prompt(experiment_data):
    return f"""You are an AI judge evaluating prompt effectiveness based on output quality. Identify the best prompt, explain why it is the best, and then refine it for clarity and effectiveness.

DATASET: {json.dumps(experiment_data, indent=2)}

Please return ONLY a JSON object with exactly three keys: "best_prompt", "reasoning", and "ultimate_prompt". Do not include any additional text or formatting."""

def call_llm(model, prompt_text):
    try:
        response = model.generate_content(prompt_text)
        return response.text.strip() if response.text else "No response."
    except Exception as e:
        print(f"❌ Error in LLM call: {e}")
        print(traceback.format_exc())
        return f"Error: {e}"

def parse_judge_json(response_text):
    try:
        # Attempt to extract a JSON object from the response
        json_str_match = re.search(r'{.*}', response_text, re.DOTALL)
        if json_str_match:
            json_str = json_str_match.group()
            return json.loads(json_str)
        else:
            raise json.JSONDecodeError("No JSON object found", response_text, 0)
    except json.JSONDecodeError:
        print("❌ ERROR: Could not parse JSON from judge response.")
        return {}

def refine_best_prompt(model, best_prompt_data):
    refinement_prompt = f"""You are tasked with refining the following prompt for clarity and effectiveness.

Best Prompt: {best_prompt_data.get('best_prompt', '').strip()}

Please return ONLY the refined prompt as a plain text string."""
    return call_llm(model, refinement_prompt).strip()

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def save_markdown(filepath, best_prompt_data):
    markdown_content = f"""# Best Prompt Selection Reasoning

## Best Prompt
{best_prompt_data.get('best_prompt', 'N/A')}

## Reasoning
{best_prompt_data.get('reasoning', 'No reasoning provided.')}

## Refined Prompt
{best_prompt_data.get('ultimate_prompt', 'N/A')}
"""
    with open(filepath, "w") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    main()
