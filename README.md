# Adaptive Prompt Refinement for Automated Requirements Analysis

An iterative pipeline that autonomously selects and refines the best prompts for generating structured requirements analysis documents.

## 🔍 Project Overview

This project explores **Dynamic Adaptive Prompt Optimization (DAPO)** to automatically generate, evaluate, and refine prompts for high-quality requirements analysis using Large Language Models (LLMs). The system applies various prompting techniques and leverages an *LLM-as-a-Judge* approach to determine the most effective prompt.

For a full research breakdown, please refer to [MY-RESEARCH.md](MY-RESEARCH.md).

## 🚀 Key Features

- **Automated Prompt Refinement**: Uses an iterative pipeline to optimize prompt engineering strategies.
- **LLM-as-a-Judge Evaluation**: Selects the best prompt based on structured criteria.
- **Comprehensive Analysis**: Evaluates Zero-Shot, Few-Shot, Chain-of-Thought (CoT), and Meta-Prompting techniques.
- **Structured Requirements Generation**: Produces high-quality requirements documents automatically.

## 🔧 How It Works

The DAPO pipeline consists of four key stages:

1. **Generate Prompt Variations** (`generator.py`)  
   Generates multiple prompt variations (Zero-Shot, Few-Shot, CoT, Meta-Prompting) with different temperatures and token limits.
2. **Evaluate & Select Best Prompt** (`judge.py`)  
   Uses an LLM to analyze prompt outputs and select the most effective one.
3. **Execute Final Best Prompt** (`executioner.py`)  
   Runs the selected "ultimate" prompt and generates the final requirements document.
4. **Final Analysis** (`jury.py`)  
   Re-evaluates all outputs to ensure the best possible selection.

For a more detailed methodology, see [MY-RESEARCH.md](MY-RESEARCH.md).

## 📥 Installation & Usage

### 1️⃣ Clone the Repository  
Run the following commands:  
- `git clone https://github.com/your-username/adaptive-prompt-refinement.git`  
- `cd adaptive-prompt-refinement`

### 2️⃣ Install Dependencies  
Run:  
- `pip install -r requirements.txt`

### 3️⃣ Run the Full Pipeline  
Run:  
- `python pipeline.py`

### 4️⃣ View Results  
Check the outputs:  
- Final requirements analysis: `artifacts/requirements_analysis.md`  
- Full experiment results: `artifacts/final_analysis_report.md`

## 📄 Research & Documentation

- **[MY-RESEARCH.md](MY-RESEARCH.md)** – Full research methodology and findings.
- **Final Analysis Report** – Detailed breakdown of prompt evaluations.
- **Generated Requirements Analysis** – Final structured requirements document.

## 📌 Contributors

- **Evan R. Parra**
- **Carl Villarosa**
- **Academic Supervisor**: Dr. Fernando Koch

## 📜 License

This project is licensed under the MIT License.

## 📌 For any inquiries, feel free to reach out or open an issue! 🚀
