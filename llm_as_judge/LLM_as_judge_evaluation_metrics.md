The document provides a comprehensive overview of evaluation metrics for Large Language Models (LLMs) acting as judges, including their definitions and formulas.

Evaluation Metrics for LLMs

Evaluation of LLM-as-a-Judge systems primarily aims to measure their alignment with human judgment and assess potential biases and robustness. The core evaluation metrics include:

1. Agreement with Human Judgment

LLM evaluators are compared with human annotations to determine their accuracy and reliability. The agreement is calculated as:

￼

where:
	•	￼ is the dataset,
	•	￼ and ￼ are evaluation scores or rankings given by the LLM and human judge, respectively.

2. Correlation Metrics

To measure how closely LLM judgments align with human evaluations, statistical correlation methods are used:
	•	Spearman’s Rank Correlation:
￼
where ￼ is the difference between LLM and human rankings for a sample, and ￼ is the number of samples.
	•	Cohen’s Kappa (Inter-rater Agreement):
￼
where ￼ is observed agreement and ￼ is expected agreement under chance.

3. Bias Evaluation Metrics

Biases in LLM evaluations are quantified to ensure fairness:
	•	Position Bias: Measures how often an LLM prefers responses in specific positions.
￼
	•	Length Bias: Evaluates if longer responses receive higher scores.
	•	Self-Enhancement Bias: Checks if LLMs prefer responses they generate.

4. Adversarial Robustness

This assesses how resilient LLM evaluations are against deliberate manipulation. A robustness metric could involve perturbation-based consistency:

￼

These metrics help improve the reliability of LLM-as-a-Judge frameworks by ensuring consistency, mitigating biases, and optimizing evaluation pipelines. Let me know if you need further clarifications!