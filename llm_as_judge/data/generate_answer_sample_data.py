import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Sample chunks and questions about data science and AI topics
chunks_and_questions = [
    {
        "chunk": "The global economy has been experiencing significant growth...",
        "question": "What factors are contributing to the global economic growth?",
        "ground_truth_answer": "Global economic growth is driven by increased industrial output, technological advancements, international trade expansion, emerging market development, and digital transformation across sectors."
    },
    {
        "chunk": "Machine learning algorithms have revolutionized data analysis...",
        "question": "How have machine learning algorithms impacted data analysis?",
        "ground_truth_answer": "Machine learning algorithms have enabled automated pattern recognition, predictive modeling, and real-time data processing at scale."
    },
    {
        "chunk": "Climate change poses significant challenges to agriculture...",
        "question": "What are the main impacts of climate change on agriculture?",
        "ground_truth_answer": "Climate change affects crop yields, growing seasons, water availability, and increases the frequency of extreme weather events impacting agricultural production."
    },
    {
        "chunk": "Artificial intelligence is transforming healthcare delivery...",
        "question": "How is AI changing healthcare delivery systems?",
        "ground_truth_answer": "AI is enabling personalized medicine, automated diagnosis, predictive healthcare analytics, and improved patient care through smart monitoring systems."
    },
    {
        "chunk": "Renewable energy adoption is accelerating globally...",
        "question": "What factors are driving renewable energy adoption?",
        "ground_truth_answer": "Cost reductions in technology, government policies, environmental concerns, and increasing energy demand are driving renewable energy adoption."
    }
]

def generate_varied_answer(ground_truth):
    """Generate a slightly modified answer with varying quality."""
    variations = [
        lambda a: a[:int(len(a)*0.7)] + "...",  # Incomplete answer
        lambda a: a.replace("and", "and also").replace(".", ". Additionally,"),  # More verbose
        lambda a: " ".join(a.split(" ")[:5]) + "...",  # Very short answer
        lambda a: a + " However, more research is needed in this area.",  # Added uncertainty
        lambda a: a,  # Original answer
        lambda a: a.replace(",", " and").replace(".", "") + " among other factors",  # Less structured
        lambda a: "Based on the context, " + a.lower(),  # More formal but redundant
        lambda a: " ".join(a.split(" ")[::2]) + "..."  # Skip words for incoherence
    ]
    return random.choice(variations)(ground_truth)

def generate_correlated_scores(base_score, variance=0.5):
    """Generate correlated scores with realistic variations."""
    # Ensure base_score is between 1 and 5
    base_score = max(1, min(5, base_score))
    
    # Generate variations around base score
    scores = {}
    metrics = ['Stand-alone Quality', 'Readiness', 'Relevance', 'Completeness']
    
    for metric in metrics:
        # Add some random variation while keeping within bounds
        llm_score = max(1, min(5, base_score + np.random.normal(0, variance)))
        # Human scores tend to have more variation
        human_score = max(1, min(5, base_score + np.random.normal(0, variance * 1.2)))
        
        scores[f'LLM {metric}'] = round(llm_score, 1)
        scores[f'Human {metric}'] = round(human_score, 1)
    
    return scores

# Generate evaluation data
data = []
for item in chunks_and_questions:
    generated_answer = generate_varied_answer(item["ground_truth_answer"])
    
    # Generate base score between 1 and 5 with tendency towards middle range
    base_score = np.random.normal(3, 0.8)
    
    # Generate all evaluation scores
    scores = generate_correlated_scores(base_score)
    
    entry = {
        'Chunk': item["chunk"],
        'Question': item["question"],
        'Answer': generated_answer,
    }
    entry.update(scores)
    data.append(entry)

# Create multiple entries for each question with different answers and scores
num_variations = 7
additional_data = []
for item in data:
    for _ in range(num_variations):
        new_entry = item.copy()
        new_entry['Answer'] = generate_varied_answer(chunks_and_questions[data.index(item)]["ground_truth_answer"])
        base_score = np.random.normal(3, 0.8)
        new_entry.update(generate_correlated_scores(base_score))
        additional_data.append(new_entry)

data.extend(additional_data)

# Create DataFrame
df = pd.DataFrame(data)

# Reorder columns to group LLM and Human scores together
metric_columns = ['Stand-alone Quality', 'Readiness', 'Relevance', 'Completeness']
column_order = ['Chunk', 'Question', 'Answer']
for metric in metric_columns:
    column_order.extend([f'LLM {metric}', f'Human {metric}'])

df = df[column_order]

# Save to CSV
df.to_csv('llm_as_judge/data/llm_judge_answer_evaluation_sample.csv', index=False) 