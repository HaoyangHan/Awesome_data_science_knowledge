import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Sample questions about various topics
ground_truth_questions = [
    "How should I create a human interactive machine?",
    "What are the key components of artificial intelligence?",
    "How does deep learning differ from machine learning?",
    "What is the role of neural networks in AI?",
    "How can we ensure AI systems are ethical?",
    "What are the applications of natural language processing?",
    "How do recommendation systems work?",
    "What is the future of autonomous vehicles?",
    "How can we implement computer vision systems?",
    "What are the challenges in robotics development?",
    "How does reinforcement learning work?",
    "What is the impact of AI on healthcare?",
    "How can we build sustainable AI systems?",
    "What are the best practices for data preprocessing?",
    "How do we evaluate machine learning models?",
    "What is the role of big data in AI?",
    "How can we optimize neural network architectures?",
    "What are the principles of responsible AI?",
    "How do we handle bias in AI systems?",
    "What is the future of human-AI collaboration?",
    "How can we improve AI model interpretability?",
    "What are the challenges in natural language understanding?",
    "How do we ensure AI privacy and security?",
    "What is the role of edge computing in AI?",
    "How can we scale AI systems effectively?",
    "What are the best practices for AI deployment?",
    "How do we maintain AI systems in production?",
    "What is the impact of AI on society?",
    "How can we make AI more energy-efficient?",
    "What are the limitations of current AI systems?",
    "How do we handle uncertainty in AI predictions?",
    "What is the role of transfer learning?",
    "How can we improve AI robustness?",
    "What are the challenges in multi-agent systems?",
    "How do we evaluate AI system performance?"
]

# Function to generate slightly modified questions
def modify_question(question):
    modifiers = [
        (lambda q: q.replace("How", "In what way")),
        (lambda q: q.replace("What", "Which")),
        (lambda q: q.replace("should", "could")),
        (lambda q: q.replace("can", "might")),
        (lambda q: q.replace("do", "should")),
        (lambda q: q.replace("are", "would be"))
    ]
    return random.choice(modifiers)(question)

# Generate data
data = {
    'Ground Truth Question': ground_truth_questions,
    'LLM Generated Question': [modify_question(q) for q in ground_truth_questions],
    'LLM Generated Score': np.random.uniform(0.5, 1.0, 35),
    'Human Evaluation Score': np.random.uniform(0.5, 0.95, 35)
}

# Create DataFrame
df = pd.DataFrame(data)

# Round scores to 2 decimal places
df['LLM Generated Score'] = df['LLM Generated Score'].round(2)
df['Human Evaluation Score'] = df['Human Evaluation Score'].round(2)

# Save to CSV
df.to_csv('llm_as_judge/data/llm_judge_evaluation_sample.csv', index=False) 