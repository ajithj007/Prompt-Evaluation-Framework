import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ── Load Data ────────────────────────────────────────
df = pd.read_csv('../data/results.csv')

print("=" * 50)
print("📊 PROMPT EVALUATION ANALYSIS REPORT")
print("=" * 50)

# ── Basic Stats ──────────────────────────────────────
print(f"\n Total evaluations: {len(df)}")
print(f"📂 Categories: {list(df['category'].unique())}")
print(f"\n🏆 Winner distribution:")
print(df['winner'].value_counts().to_string())

# ── Overall Averages ─────────────────────────────────
print("\n" + "=" * 50)
print(" OVERALL AVERAGES")
print("=" * 50)
print(f"Prompt A average score: {df['average_a'].mean():.2f}")
print(f"Prompt B average score: {df['average_b'].mean():.2f}")
better = 'B' if df['average_b'].mean() > df['average_a'].mean() else 'A'
print(f"\n Overall better prompt style: Prompt {better}")

# ── Category Analysis ────────────────────────────────
print("\n" + "=" * 50)
print(" SCORES BY CATEGORY")
print("=" * 50)
category_analysis = df.groupby('category').agg({
    'average_a': 'mean',
    'average_b': 'mean'
}).round(2)
category_analysis['winner'] = category_analysis.apply(
    lambda x: 'B' if x['average_b'] > x['average_a'] else 'A', axis=1
)
print(category_analysis.to_string())

# ── Criteria Breakdown ───────────────────────────────
print("\n" + "=" * 50)
print(" CRITERIA BREAKDOWN")
print("=" * 50)
criteria = ['relevance', 'clarity', 'completeness', 'conciseness']
for c in criteria:
    a = df[f'{c}_a'].mean()
    b = df[f'{c}_b'].mean()
    winner = 'B' if b > a else 'A'
    print(f"{c.capitalize():15} A: {a:.2f}  B: {b:.2f}  → Winner: {winner}")

# ── Key Insights ─────────────────────────────────────
print("\n" + "=" * 50)
print(" KEY INSIGHTS")
print("=" * 50)
b_wins = (df['winner'] == 'B').sum()
a_wins = (df['winner'] == 'A').sum()
print(f"1. Prompt B (detailed) won {b_wins}/{len(df)} evaluations")
print(f"   Prompt A (simple) won {a_wins}/{len(df)} evaluations")

best_cat = category_analysis['average_b'].idxmax()
print(f"\n2. Detailed prompts work best for: {best_cat}")

criteria_diff = {
    'Relevance': df['relevance_b'].mean() - df['relevance_a'].mean(),
    'Clarity': df['clarity_b'].mean() - df['clarity_a'].mean(),
    'Completeness': df['completeness_b'].mean() - df['completeness_a'].mean(),
    'Conciseness': df['conciseness_b'].mean() - df['conciseness_a'].mean()
}
best_criteria = max(criteria_diff, key=criteria_diff.get)
print(f"\n3. Biggest improvement area: {best_criteria}")
print(f"   Difference: +{criteria_diff[best_criteria]:.2f} points")

# ── Generate Charts ──────────────────────────────────
print("\nGenerating charts...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Prompt Evaluation Analysis Report',
             fontsize=16, fontweight='bold')

# Chart 1 - Overall comparison
axes[0,0].bar(['Prompt A\n(Simple)', 'Prompt B\n(Detailed)'],
              [df['average_a'].mean(), df['average_b'].mean()],
              color=['#3498db', '#e74c3c'])
axes[0,0].set_title('Overall Average Scores')
axes[0,0].set_ylabel('Score (out of 10)')
axes[0,0].set_ylim(0, 10)
for i, v in enumerate([df['average_a'].mean(), df['average_b'].mean()]):
    axes[0,0].text(i, v + 0.1, f'{v:.2f}', ha='center', fontweight='bold')

# Chart 2 - Winner pie chart
winner_counts = df['winner'].value_counts()
axes[0,1].pie(winner_counts.values,
              labels=[f'Prompt {x}\n({v} wins)'
                      for x, v in winner_counts.items()],
              autopct='%1.1f%%',
              colors=['#3498db', '#e74c3c'],
              startangle=90)
axes[0,1].set_title('Win Distribution')

# Chart 3 - Category comparison
cat_scores = df.groupby('category')[['average_a', 'average_b']].mean()
x = range(len(cat_scores))
axes[1,0].bar([i - 0.2 for i in x], cat_scores['average_a'],
              width=0.4, label='Prompt A', color='#3498db')
axes[1,0].bar([i + 0.2 for i in x], cat_scores['average_b'],
              width=0.4, label='Prompt B', color='#e74c3c')
axes[1,0].set_xticks(x)
axes[1,0].set_xticklabels(cat_scores.index, rotation=15, ha='right')
axes[1,0].set_title('Scores by Category')
axes[1,0].set_ylabel('Score')
axes[1,0].set_ylim(0, 10)
axes[1,0].legend()

# Chart 4 - Criteria line comparison
criteria_labels = ['Relevance', 'Clarity', 'Completeness', 'Conciseness']
scores_a = [df['relevance_a'].mean(), df['clarity_a'].mean(),
            df['completeness_a'].mean(), df['conciseness_a'].mean()]
scores_b = [df['relevance_b'].mean(), df['clarity_b'].mean(),
            df['completeness_b'].mean(), df['conciseness_b'].mean()]
axes[1,1].plot(criteria_labels, scores_a, 'o-',
               label='Prompt A', color='#3498db', linewidth=2)
axes[1,1].plot(criteria_labels, scores_b, 's-',
               label='Prompt B', color='#e74c3c', linewidth=2)
axes[1,1].set_title('Criteria Breakdown')
axes[1,1].set_ylabel('Score')
axes[1,1].set_ylim(0, 10)
axes[1,1].legend()
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../data/analysis_charts.png', dpi=150, bbox_inches='tight')
plt.show()
print("Charts saved to data/analysis_charts.png")
