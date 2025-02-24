![GenI-banner](https://github.com/genilab-fau/genilab-fau.github.io/blob/8d6ab41403b853a273983e4c06a7e52229f43df5/images/genilab-banner.png?raw=true)

# Adaptive Prompt Refinement for Automated Requirements Analysis

An iterative pipeline that automatically selects and refines prompts for high-quality requirement documents.

- **Authors**: Evan R. Parra, Carl Villarosa  
- **Academic Supervisor**: [Dr. Fernando Koch](http://www.fernandokoch.me)

---

# Research Question

**How can we autonomously select and refine the best prompt for generating structured requirements analyses, minimizing human intervention while maximizing accuracy and clarity?**

---

## Arguments

### What is already known about this topic

- The **Software Development Lifecycle (SDLC)** requires well-defined requirements to ensure alignment with business needs [1].
- **Prompt engineering** for Large Language Models (LLMs) is challenging due to variations in parameter tuning (temperature, tokens, prompt structure, etc.) [2].
- Techniques like **Chain-of-Thought (CoT)** prompting have proven beneficial in guiding LLM outputs [3].

### What this research is exploring

We develop a **Dynamic Adaptive Prompt Optimization (DAPO)** pipeline that:

1. **Generates multiple prompt variations**: Utilizing Zero-Shot, Few-Shot, CoT, and Meta-Prompting across different parameters.
2. **Evaluates outputs**: Using an LLM-as-a-Judge framework to identify the most structured and complete requirements analysis [1].
3. **Refines the best prompt**: Iteratively optimizing an "ultimate" prompt for final execution.

### Implications for practice

- **Reduced manual workload**: Automating prompt selection and refinement accelerates the SDLC's requirement analysis phase [4].
- **Consistency**: LLM-as-a-Judge ensures uniformity in the structure and completeness of requirement documents.
- **Continuous improvement**: The pipeline iterates over multiple refinements, potentially discovering better strategies over time [2].

---

# Research Method

### **DAPO Pipeline Overview**

This project implements a multi-stage process that autonomously refines prompts for optimal requirements analysis generation. The workflow consists of four key steps:

1. **Prompt Variation (`generator.py`)**
   - Generates 36 combinations of prompts (4 techniques × 3 temperatures × 3 max tokens).
   - Stores results in Firestore for tracking.
   
2. **LLM-as-a-Judge (`judge.py`)**
   - Compares all outputs and selects the best-performing prompt.
   - Optionally refines the prompt to enhance clarity and completeness.

3. **Execution (`executioner.py`)**
   - Runs the "ultimate" prompt to generate the final requirements analysis.
   - Appends the new output to `experiment_results.csv`.

4. **Final Analysis (`jury.py`)**
   - Re-evaluates all results, ensuring the best possible prompt was selected.
   - Highlights runner-ups and suboptimal approaches.

---

# **Results**

### **Ultimate Best Prompt**

After evaluating all prompt variations, the **ultimate prompt** was identified as the most effective for generating a structured requirements analysis:

> **Generate a comprehensive Requirement Analysis document using the following structured approach:**  
> 1. **Data Sources**: Identify all key data sources the system will utilize.  
> 2. **Financial Data Processing**: Describe the extraction and processing of financial data.  
> 3. **Financial Ratio Calculation**: Explain how key financial ratios are computed.  
> 4. **Sentiment Analysis**: Detail the application of sentiment analysis.  
> 5. **Recommendation Logic**: Describe the logic behind Buy, Hold, and Sell recommendations.  
> 6. **User Interface**: Define the user interface and expected user interactions.  

This structured approach ensures **clarity, depth, and logical flow**, outperforming other methods in comprehensiveness.

### **Key Findings**

- **Chain-of-Thought (CoT) Prompting**
  - Effectively guided structured output but lacked depth in user interaction details.
- **Zero-Shot Prompting**
  - Provided quick results but lacked structure and depth.
- **Few-Shot Prompting**
  - Improved over Zero-Shot but still required refinement.
- **Meta-Prompting**
  - Useful for gathering clarifications but deviated from the primary objective of requirement generation.

**Common Challenges:**
- **Insufficient token limits** resulted in truncated analyses.
- **High-temperature settings** led to inconsistencies.
- **Lack of specificity** caused generic outputs.

For a more in-depth analysis of the experimental results and prompt evaluations, refer to the **[Final Analysis Report](artifacts/final_analysis_report.md)**.

---

# Generated Requirements Analysis

The final Requirements Analysis document, produced using the ultimate prompt, can be viewed here:

📄 **[View the Generated Requirements Analysis](artifacts/requirements_analysis.md)**

---

# Conclusion & Future Work

### **Lessons Learned**
- **Explicit structuring improves LLM responses** → Prompting step-by-step enhances coherence.
- **Temperature control is critical** → Lower values ensure stability, while higher ones introduce variability.
- **Iterative refinement maximizes quality** → The best results come from systematic experimentation.

### **Next Steps**
- **Refine CoT-based approaches** → Enhance structured breakdown for more depth.
- **Explore domain-specific fine-tuning** → Improve performance for financial and regulatory applications.
- **Expand to other SDLC phases** → Apply DAPO beyond requirements analysis.

---

# References

[1] L. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," *arXiv preprint* arXiv:2306.05685, 2023. [Online]. Available: [https://arxiv.org/abs/2306.05685](https://arxiv.org/abs/2306.05685)  
[2] P. Ke et al., "CritiqueLLM: Scaling LLM-as-Critic for Effective and Explainable Evaluation of Large Language Model Generation," *arXiv preprint* arXiv:2311.18702, 2023. [Online]. Available: [https://arxiv.org/abs/2311.18702](https://arxiv.org/abs/2311.18702)  
[3] A. S. Thakur et al., "Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges," *arXiv preprint* arXiv:2406.12624, 2024. [Online]. Available: [https://arxiv.org/abs/2406.12624](https://arxiv.org/abs/2406.12624)  
[4] Z. Gou et al., "CRITIC: Large Language Models Can Self-Correct with Tool-Use," *ICLR 2024 Conference Proceedings*, 2024. [Online]. Available: [https://openreview.net/forum?id=Sx038qxjek](https://openreview.net/forum?id=Sx038qxjek)
