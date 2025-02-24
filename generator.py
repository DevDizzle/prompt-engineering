#!/usr/bin/env python3
"""
generator.py
------------
Generates multiple prompt variations, evaluates outputs, and saves:
  - experiment_results.csv (inside artifacts/)
  - Stores results in Firestore (for cloud tracking)
"""

import os
import time
import json
import pandas as pd
from google.cloud import firestore
import google.generativeai as genai

# Initialize Firestore
db = firestore.Client()

# Retrieve the API key from system environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ ERROR: GEMINI_API_KEY environment variable not set.")

# Configure Gemini 1.5 Pro Model
genai.configure(api_key=api_key)

# Define the model
model = genai.GenerativeModel("gemini-1.5-pro")

# Experiment configurations
prompt_types = {
    "zero_shot": "Generate a Requirement Analysis for a system that provides stock recommendations based on financial ratios "
                 "and sentiment analysis of MD&A sections from 10-K filings. Outline the system's functional and non-functional "
                 "requirements, data sources, key processing components, and user interactions.",
    
    "few_shots": "Example 1: A stock analysis system that only uses financial ratios would: - Extract financial data from SEC 10-K filings. "
                 "- Compute profitability, liquidity, and solvency ratios. - Recommend Buy, Hold, or Sell based on predefined thresholds.\n\n"
                 "Example 2: A sentiment-based system would: - Analyze MD&A sections for positive or negative sentiment. "
                 "- Score sentiment and combine it with financial metrics.\n\n"
                 "Now, generate a Requirement Analysis for a system that integrates both approaches.",
    
    "cot": "To generate a complete Requirement Analysis, let’s break it down step by step:\n\n"
           "Step 1: Identify key data sources for the system.\n"
           "Step 2: Describe how financial data is extracted and processed.\n"
           "Step 3: Explain how financial ratios are computed.\n"
           "Step 4: Detail how sentiment analysis is applied.\n"
           "Step 5: Describe the recommendation logic for Buy, Hold, and Sell.\n"
           "Step 6: Define the user interface and expected user interactions.\n\n"
           "Now, generate a structured Requirement Analysis using this step-by-step approach.",
    
    "meta_prompting": "Before generating a Requirement Analysis, ask three clarifying questions to refine the analysis. "
                      "After answering those questions, use the refined information to generate a structured Requirement Analysis."
}

temperatures = [0.3, 0.5, 0.7]
max_tokens = [512, 768, 1024]

# Ensure artifacts directory exists
artifacts_dir = "artifacts"
if not os.path.exists(artifacts_dir):
    os.makedirs(artifacts_dir)

# Path for storing CSV output
csv_file_path = os.path.join(artifacts_dir, "experiment_results.csv")

# Store results for CSV export
results = []

# Function to run a single experiment
def run_experiment(prompt_type, prompt_text, temp, max_tok):
    print(f"🚀 Running: {prompt_type} | Temp: {temp} | Max Tokens: {max_tok}")

    try:
        # Generate content with Gemini 1.5 Pro
        response = model.generate_content(
            prompt_text,
            generation_config={
                "temperature": temp,
                "max_output_tokens": max_tok
            }
        )
        response_text = response.text.strip() if response.text else "No Response"
    except Exception as e:
        response_text = f"Error: {e}"

    # Store result in Firestore
    db.collection("prompt_experiments").add({
        "prompt_type": prompt_type,
        "actual_prompt": prompt_text,
        "temperature": temp,
        "max_tokens": max_tok,
        "response_text": response_text,
        "timestamp": time.time()
    })

    # Store in list for CSV export
    results.append([prompt_type, prompt_text, temp, max_tok, response_text])

# Run all experiments
for prompt_type, prompt_text in prompt_types.items():
    for temp in temperatures:
        for max_tok in max_tokens:
            run_experiment(prompt_type, prompt_text, temp, max_tok)
            time.sleep(2)  # Avoid API rate limits

# Export results to CSV in the artifacts directory
df = pd.DataFrame(results, columns=["Prompt Type", "Actual Prompt", "Temperature", "Max Tokens", "Response Text"])
df.to_csv(csv_file_path, index=False)

print(f"✅ Experimentation Complete! Results exported to: {csv_file_path}")

# Verify file creation
if os.path.isfile(csv_file_path):
    print(f"✅ File successfully written: {csv_file_path}")
else:
    print(f"❌ ERROR: experiment_results.csv not found in {artifacts_dir}")
