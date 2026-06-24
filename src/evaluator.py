import anthropic
import os
import csv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_response(prompt, model="claude-haiku-4-5-20251001"):
    """Send prompt to Claude and get response"""
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

def score_response(response, task, model="claude-haiku-4-5-20251001"):
    """Ask Claude to score a response on 4 criteria"""
    scoring_prompt = f"""
    Task given to AI: {task}
    AI Response: {response}
    
    Score this response on these 4 criteria from 1-10:
    1. Relevance: Did it answer the task?
    2. Clarity: Is it easy to understand?
    3. Completeness: Did it cover everything needed?
    4. Conciseness: Is it the right length?
    
    Reply in this exact format only, nothing else:
    Relevance: X
    Clarity: X
    Completeness: X
    Conciseness: X
    """
    score_message = client.messages.create(
        model=model,
        max_tokens=100,
        messages=[
            {"role": "user", "content": scoring_prompt}
        ]
    )
    return score_message.content[0].text

def parse_scores(score_text):
    """Convert score text to numbers"""
    scores = {}
    try:
        for line in score_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':')
                scores[key.strip()] = float(value.strip())
        scores['Average'] = sum(scores.values()) / len(scores)
    except Exception as e:
        print(f"Score parsing error: {e}")
        scores = {
            'Relevance': 0, 'Clarity': 0,
            'Completeness': 0, 'Conciseness': 0,
            'Average': 0
        }
    return scores

def save_results(task, category, prompt_a, prompt_b,
                 response_a, response_b,
                 scores_a, scores_b):
    """Save results to CSV"""
    filepath = '../data/results.csv'
    file_exists = os.path.exists(filepath) and \
                  os.path.getsize(filepath) > 0

    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                'timestamp', 'task', 'category',
                'prompt_a', 'prompt_b',
                'response_a', 'response_b',
                'relevance_a', 'clarity_a',
                'completeness_a', 'conciseness_a', 'average_a',
                'relevance_b', 'clarity_b',
                'completeness_b', 'conciseness_b', 'average_b',
                'winner'
            ])

        winner = 'A' if scores_a['Average'] > scores_b['Average'] else 'B'

        writer.writerow([
            datetime.now(), task, category,
            prompt_a, prompt_b,
            response_a, response_b,
            scores_a.get('Relevance', 0),
            scores_a.get('Clarity', 0),
            scores_a.get('Completeness', 0),
            scores_a.get('Conciseness', 0),
            scores_a['Average'],
            scores_b.get('Relevance', 0),
            scores_b.get('Clarity', 0),
            scores_b.get('Completeness', 0),
            scores_b.get('Conciseness', 0),
            scores_b['Average'],
            winner
        ])
    print(f"✅ Results saved to {filepath}")

def evaluate(task, category, prompt_a, prompt_b):
    """Main function — run full evaluation"""
    print(f"\n🔍 Task: {task}")
    print(f"📂 Category: {category}")
    print("-" * 50)

    print("⏳ Getting response for Prompt A...")
    response_a = get_response(prompt_a)

    print("⏳ Getting response for Prompt B...")
    response_b = get_response(prompt_b)

    print("📊 Scoring Prompt A...")
    scores_a = parse_scores(score_response(response_a, task))

    print("📊 Scoring Prompt B...")
    scores_b = parse_scores(score_response(response_b, task))

    save_results(task, category, prompt_a, prompt_b,
                response_a, response_b,
                scores_a, scores_b)

    print("\n📊 RESULTS:")
    print(f"Prompt A Average: {scores_a['Average']:.2f}")
    print(f"Prompt B Average: {scores_b['Average']:.2f}")
    winner = 'A' if scores_a['Average'] > scores_b['Average'] else 'B'
    print(f"🏆 Winner: Prompt {winner}")
    print("-" * 50)

    return scores_a, scores_b

# ── Run multiple test cases ──────────────────────────
if __name__ == "__main__":

    test_cases = [
        {
            "task": "Explain what machine learning is",
            "category": "Technical Explanation",
            "prompt_a": "What is machine learning?",
            "prompt_b": "Explain machine learning in simple terms with a real life example for a beginner."
        },
        {
            "task": "Write a professional email requesting a meeting",
            "category": "Writing",
            "prompt_a": "Write an email to request a meeting.",
            "prompt_b": "Write a professional, concise email to a senior manager requesting a 30-minute meeting to discuss project progress. Use a formal but friendly tone."
        },
        {
            "task": "Summarize the importance of data science",
            "category": "Summarization",
            "prompt_a": "Summarize data science importance.",
            "prompt_b": "Write a 3-sentence summary of why data science is important in today's world, focusing on business and social impact."
        },
        {
            "task": "Explain Python lists",
            "category": "Technical Explanation",
            "prompt_a": "What are Python lists?",
            "prompt_b": "Explain Python lists to a complete beginner with a simple code example and explain what the output means."
        },
        {
            "task": "Give tips for a job interview",
            "category": "Advice",
            "prompt_a": "Give interview tips.",
            "prompt_b": "Give 5 specific, actionable tips for a fresher attending their first technical job interview at an IT company."
        },
        {
            "task": "Explain what SQL is",
            "category": "Technical Explanation",
            "prompt_a": "What is SQL?",
            "prompt_b": "Explain SQL to someone who has never coded before, using a simple real-world analogy and one basic example query."
        },
        {
            "task": "Write a product description",
            "category": "Writing",
            "prompt_a": "Write a product description for a water bottle.",
            "prompt_b": "Write a compelling 50-word product description for an eco-friendly stainless steel water bottle targeting health-conscious young adults."
        },
        {
            "task": "Explain climate change",
            "category": "General Explanation",
            "prompt_a": "What is climate change?",
            "prompt_b": "Explain climate change in simple language suitable for a 15-year-old, including one cause, one effect, and one solution."
        },
        {
            "task": "Explain the differnce between supervised and unsupervised learning",
            "category": "Learning",
            "prompt_a": "explain supervised and unsupervised learning",
            "prompt_b": "explain the key differences between supervised and unsuperised learning for greater mark in points"
        }
    ]

    print("🚀 Starting Prompt Evaluation Framework")
    print(f"📋 Running {len(test_cases)} evaluations...\n")

    for i, case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}]")
        evaluate(
            task=case["task"],
            category=case["category"],
            prompt_a=case["prompt_a"],
            prompt_b=case["prompt_b"]
        )

    print("\n✅ All evaluations complete!")
    print("📁 Check data/results.csv for full results")