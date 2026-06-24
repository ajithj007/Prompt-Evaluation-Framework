import anthropic
import os
import csv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_response(prompt):
    """Send prompt to Claude and get response"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

def score_response(response, task):
    """Ask Claude to score a response on 4 criteria"""
    scoring_prompt = f"""
    Task given to AI: {task}
    AI Response: {response}
    
    Score this response on these 4 criteria from 1-10:
    1. Relevance: Did it answer the task?
    2. Clarity: Is it easy to understand?
    3. Completeness: Did it cover everything needed?
    4. Conciseness: Is it the right length, not too long or short?
    
    Reply in this exact format only, nothing else:
    Relevance: X
    Clarity: X
    Completeness: X
    Conciseness: X
    """
    
    score_message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[
            {"role": "user", "content": scoring_prompt}
        ]
    )
    return score_message.content[0].text

def parse_scores(score_text):
    """Convert score text to numbers"""
    scores = {}
    for line in score_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':')
            scores[key.strip()] = float(value.strip())
    scores['Average'] = sum(scores.values()) / len(scores)
    return scores

def save_results(task, prompt_a, prompt_b, 
                 response_a, response_b, 
                 scores_a, scores_b):
    """Save results to CSV"""
    with open('data/results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if file is empty
        if f.tell() == 0:
            writer.writerow([
                'timestamp', 'task',
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
            datetime.now(), task,
            prompt_a, prompt_b,
            response_a, response_b,
            scores_a['Relevance'], scores_a['Clarity'],
            scores_a['Completeness'], scores_a['Conciseness'],
            scores_a['Average'],
            scores_b['Relevance'], scores_b['Clarity'],
            scores_b['Completeness'], scores_b['Conciseness'],
            scores_b['Average'],
            winner
        ])

def evaluate(task, prompt_a, prompt_b):
    """Main function — run full evaluation"""
    print(f"\n🔍 Evaluating prompts for task: {task}")
    print("-" * 50)
    
    # Get responses
    print("Getting response for Prompt A...")
    response_a = get_response(prompt_a)
    
    print("Getting response for Prompt B...")
    response_b = get_response(prompt_b)
    
    # Score responses
    print("Scoring Prompt A...")
    scores_a = parse_scores(score_response(response_a, task))
    
    print("Scoring Prompt B...")
    scores_b = parse_scores(score_response(response_b, task))
    
    # Save results
    save_results(task, prompt_a, prompt_b,
                response_a, response_b,
                scores_a, scores_b)
    
    # Print results
    print("\n📊 RESULTS:")
    print(f"Prompt A Average Score: {scores_a['Average']:.2f}")
    print(f"Prompt B Average Score: {scores_b['Average']:.2f}")
    winner = 'A' if scores_a['Average'] > scores_b['Average'] else 'B'
    print(f"\n🏆 Best Prompt: Prompt {winner}")
    
    return scores_a, scores_b

# Test it
if __name__ == "__main__":
    evaluate(
        task="Explain what machine learning is",
        prompt_a="What is machine learning?",
        prompt_b="Explain machine learning in simple terms with a real life example, suitable for a beginner with no technical background."
    )
