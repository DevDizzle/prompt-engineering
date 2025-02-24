#!/usr/bin/env python3
"""
jury.py
-------
Loads artifacts/experiment_results.csv (including the new 'ultimate' row)
and asks Gemini 1.5 Pro for a final analysis:
 - Does the 'ultimate' prompt truly remain best?
 - Which runner-ups are interesting?
 - Any general observations about suboptimal outcomes, etc.

Outputs a structured Markdown report to artifacts/final_analysis_report.md.
"""

import os
import json
import pandas as pd
import traceback
import google.generativeai as genai

def main():
    # Ensure artifacts directory exists
    artifacts_dir = "artifacts"
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)

    # Define paths to required files
    csv_file_path = os.path.join(artifacts_dir, "experiment_results.csv")
    markdown_file_path = os.path.join(artifacts_dir, "final_analysis_report.md")

    # Debugging: Confirm paths before execution
    print(f"🔍 Checking required files:")
    print(f"   - CSV Input: {csv_file_path}")
    print(f"   - Markdown Output: {markdown_file_path}")

    # 1) Read experiment_results.csv
    if not os.path.isfile(csv_file_path):
        raise FileNotFoundError(f"❌ ERROR: '{csv_file_path}' not found. Run generator.py first.")

    df = pd.read_csv(csv_file_path)

    # Ensure the dataset is not empty
    if df.empty:
        raise ValueError(f"❌ ERROR: '{csv_file_path}' is empty. Check if generator.py ran correctly.")

    experiment_data = df.to_dict(orient="records")

    # 2) Configure Gemini 1.5 Pro
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ ERROR: GEMINI_API_KEY not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

    # 3) Build the final analysis prompt
    final_analysis_prompt = build_final_analysis_prompt(experiment_data)

    # 4) Call the LLM with a higher max token limit
    final_analysis_text = call_llm(
        model=model,
        prompt_text=final_analysis_prompt,
        temperature=0.2,  # Keep low for analysis
        max_tokens=2048  # Increased from 1024 to avoid truncation
    )

    # Ensure response is valid
    if "Error:" in final_analysis_text or final_analysis_text.strip() == "":
        raise ValueError("❌ ERROR: LLM response was empty or contained an error.")

    # 5) Save the analysis in Markdown format
    save_markdown(markdown_file_path, final_analysis_text)

    print(f"\n✅ jury.py: Successfully created '{markdown_file_path}'.\n")
    print("🔍 Analysis Preview:\n")
    print(final_analysis_text[:500], "...\n")  # Print first 500 chars as a preview

    # Verify Markdown file exists after writing
    if os.path.isfile(markdown_file_path):
        print(f"✅ Verified: {markdown_file_path} exists.")
    else:
        print(f"❌ ERROR: Markdown file missing after writing. Check jury.py.")

def build_final_analysis_prompt(experiment_data):
    """
    Construct a prompt that instructs the LLM to re-evaluate the entire dataset,
    focusing on whether the 'ultimate' prompt truly remains best, 
    or if there are any interesting runner-ups or issues with other techniques.
    """

    prompt = f"""
You are a senior AI consultant. You have the final experiment data from multiple prompt engineering runs,
including a newly added 'ultimate' prompt. Please perform a thorough final analysis:

1) Evaluate if the 'ultimate' prompt truly delivers the best Requirements Analysis outcome.
2) Identify any interesting runner-ups or suboptimal approaches.
3) Discuss how different prompt engineering strategies (Zero-Shot, Few-Shots, CoT, Meta-Prompting) compare,
   referencing any common mistakes or noteworthy highlights from the dataset.
4) Offer overall recommendations or lessons learned about prompt engineering for requirements analysis.

DATASET (each row includes 'Prompt Type', 'Actual Prompt', 'Temperature', 'Max Tokens', 'Response Text'):
{json.dumps(experiment_data, indent=2)}

Output a detailed analysis as a structured Markdown document with headings and bullet points.
"""
    return prompt.strip()

def call_llm(model, prompt_text, temperature, max_tokens):
    """
    Calls Gemini 1.5 Pro with the final analysis prompt. Returns a textual commentary.
    """
    try:
        response = model.generate_content(
            prompt_text,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )

        if response.text:
            print(f"✅ Analysis Preview (First 200 chars): {response.text.strip()[:200]}...")

        return response.text.strip() if response.text else "No analysis produced."

    except Exception as e:
        print(f"❌ ERROR: LLM call failed: {e}")
        print(traceback.format_exc())  
        return f"Error: {e}"

def save_markdown(filepath, content):
    """
    Saves the final analysis as a structured Markdown file.
    """
    markdown_content = f"""# Final Analysis Report: Prompt Engineering Evaluation

## 📌 Summary
{content}

---

*Generated automatically using Gemini 1.5 Pro*
"""

    with open(filepath, "w") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    main()
