"""
Generate publication-quality figures for Sepsis HDT Pipeline
Author: Dr. Siddalingaiah H S
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
plt.style.use('seaborn-v0_8-whitegrid')

def figure1_target_prioritization():
    """Figure 1: Top 20 Target Prioritization with Phase Coloring"""
    df = pd.read_csv(BASE_DIR / 'outputs' / 'tables' / 'targets_ranked.csv')
    top20 = df.head(20)
    
    # Color by phase
    phase_colors = {'Early': '#E74C3C', 'Late': '#3498DB', 'Both': '#9B59B6'}
    colors = [phase_colors[p] for p in top20['Phase_Relevance']]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(range(len(top20)), top20['Composite_Score'], color=colors, edgecolor='black', linewidth=0.5)
    
    ax.set_yticks(range(len(top20)))
    ax.set_yticklabels(top20['Symbol'], fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    
    ax.set_xlabel('Composite Score', fontsize=12, fontweight='bold')
    ax.set_title('Top 20 Host-Directed Therapy Targets for Sepsis\n(Colored by Immune Phase)', fontsize=14, fontweight='bold')
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, top20['Composite_Score'])):
        ax.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=9)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#E74C3C', label='Early Phase (Hyperinflammation)'),
        Patch(facecolor='#3498DB', label='Late Phase (Immunosuppression)'),
        Patch(facecolor='#9B59B6', label='Both Phases')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure1_target_prioritization.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure1_target_prioritization.png")

def figure2_compound_distribution():
    """Figure 2: Compound Distribution by Clinical Phase and Target"""
    df = pd.read_csv(BASE_DIR / 'outputs' / 'tables' / 'compounds_ranked.csv')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # A: Clinical phase distribution
    phase_counts = df['Phase'].value_counts().sort_index(ascending=False)
    phase_labels = {4: 'Approved (FDA)', 3: 'Phase III', 2: 'Phase II', 1: 'Phase I'}
    
    colors = ['#27AE60', '#F1C40F', '#E67E22', '#E74C3C']
    wedges, texts, autotexts = axes[0].pie(
        phase_counts.values, 
        labels=[phase_labels.get(p, f'Phase {p}') for p in phase_counts.index],
        autopct='%1.1f%%',
        colors=colors[:len(phase_counts)],
        explode=[0.05 if p == 4 else 0 for p in phase_counts.index],
        shadow=True
    )
    axes[0].set_title('A. Clinical Development Phase\n(n={})'.format(len(df)), fontsize=12, fontweight='bold')
    
    # B: Compounds by target pathway
    target_counts = df.groupby('Related_Gene').size().sort_values(ascending=True).tail(10)
    
    axes[1].barh(range(len(target_counts)), target_counts.values, color='steelblue', edgecolor='black')
    axes[1].set_yticks(range(len(target_counts)))
    axes[1].set_yticklabels(target_counts.index, fontsize=10)
    axes[1].set_xlabel('Number of Compounds', fontsize=11)
    axes[1].set_title('B. Compounds per Target Gene', fontsize=12, fontweight='bold')
    
    for i, v in enumerate(target_counts.values):
        axes[1].text(v + 0.1, i, str(v), va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure2_compound_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure2_compound_distribution.png")

def figure3_potency_by_target():
    """Figure 3: Compound Potency Distribution by Target"""
    df = pd.read_csv(BASE_DIR / 'outputs' / 'tables' / 'compounds_ranked.csv')
    
    # Get mean potency by target
    potency_by_gene = df.groupby('Related_Gene')['pChEMBL'].agg(['mean', 'max', 'count'])
    potency_by_gene = potency_by_gene.sort_values('max', ascending=False).head(15)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(potency_by_gene)))
    
    bars = ax.barh(range(len(potency_by_gene)), potency_by_gene['max'], color=colors, edgecolor='black')
    
    ax.set_yticks(range(len(potency_by_gene)))
    ax.set_yticklabels(potency_by_gene.index, fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    
    ax.set_xlabel('Maximum pChEMBL (Higher = More Potent)', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Targets by Maximum Compound Potency', fontsize=14, fontweight='bold')
    
    # Add threshold lines
    ax.axvline(x=6.0, color='red', linestyle='--', alpha=0.7, label='1 µM threshold')
    ax.axvline(x=8.0, color='green', linestyle='--', alpha=0.7, label='10 nM threshold')
    
    # Value labels
    for i, (idx, row) in enumerate(potency_by_gene.iterrows()):
        ax.text(row['max'] + 0.1, i, f'{row["max"]:.1f} (n={int(row["count"])})', va='center', fontsize=9)
    
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure3_target_potency.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure3_target_potency.png")

def figure4_pathway_heatmap():
    """Figure 4: Pathway Analysis Heatmap"""
    df = pd.read_csv(BASE_DIR / 'outputs' / 'tables' / 'targets_ranked.csv')
    
    # Create pathway summary
    pathway_summary = df.groupby(['Pathway', 'Phase_Relevance']).agg({
        'Composite_Score': 'mean',
        'Symbol': 'count',
        'PubMed_Count': 'sum'
    }).reset_index()
    
    # Pivot for heatmap
    pivot_score = df.pivot_table(
        values='Composite_Score', 
        index='Pathway', 
        columns='Phase_Relevance', 
        aggfunc='mean'
    ).fillna(0)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    
    # A: Score heatmap by pathway and phase
    sns.heatmap(pivot_score, annot=True, fmt='.3f', cmap='RdYlGn', 
                ax=axes[0], cbar_kws={'label': 'Mean Composite Score'})
    axes[0].set_title('A. Mean Target Score by Pathway and Phase', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Immune Phase', fontsize=11)
    axes[0].set_ylabel('Pathway', fontsize=11)
    
    # B: Targets per pathway
    pathway_counts = df.groupby('Pathway').size().sort_values(ascending=True)
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(pathway_counts)))
    axes[1].barh(range(len(pathway_counts)), pathway_counts.values, color=colors, edgecolor='black')
    axes[1].set_yticks(range(len(pathway_counts)))
    axes[1].set_yticklabels(pathway_counts.index, fontsize=10)
    axes[1].set_xlabel('Number of Targets', fontsize=11)
    axes[1].set_title('B. Target Distribution by Pathway', fontsize=12, fontweight='bold')
    
    for i, v in enumerate(pathway_counts.values):
        axes[1].text(v + 0.1, i, str(v), va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure4_pathway_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure4_pathway_heatmap.png")

def figure5_sepsis_timeline():
    """Figure 5: Sepsis Immune Response Timeline with HDT Opportunities"""
    fig, ax = plt.subplots(figsize=(14, 9))  # Increased height
    
    # Timeline
    time_points = [0, 24, 48, 72, 120, 168]
    
    # Inflammatory response curve
    x = np.linspace(0, 168, 500)
    inflammation = 100 * np.exp(-0.015 * (x - 24)**2 / 100) * (1 + 0.3 * np.sin(x/10))
    inflammation[x < 6] = inflammation[x < 6] * (x[x < 6] / 6)
    
    # Immunosuppression curve
    immunosuppression = 80 * (1 - np.exp(-0.02 * x)) * np.exp(-0.003 * x)
    
    ax.fill_between(x, 0, inflammation, alpha=0.3, color='red', label='Hyperinflammation')
    ax.fill_between(x, 0, immunosuppression, alpha=0.3, color='blue', label='Immunosuppression')
    ax.plot(x, inflammation, 'r-', linewidth=2)
    ax.plot(x, immunosuppression, 'b-', linewidth=2)
    
    # Annotate phases
    ax.annotate('CYTOKINE\\nSTORM', xy=(30, 75), fontsize=11, fontweight='bold', color='darkred', ha='center')
    ax.annotate('IMMUNE\\nPARALYSIS', xy=(120, 45), fontsize=11, fontweight='bold', color='darkblue', ha='center')
    
    # HDT intervention arrows - positioned lower
    ax.annotate('', xy=(24, 85), xytext=(24, 100),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(24, 103, 'Anti-IL6\\nNLRP3 inhibitors\\nJAK inhibitors', ha='center', fontsize=9, color='green')
    
    ax.annotate('', xy=(100, 50), xytext=(100, 65),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2))
    ax.text(100, 68, 'Checkpoint inhibitors\\nGM-CSF\\nIL-7', ha='center', fontsize=9, color='purple')
    
    ax.set_xlabel('Time from Sepsis Onset (hours)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Immune Response Intensity', fontsize=12, fontweight='bold')
    ax.set_title('Sepsis Immune Response Timeline and HDT Intervention Windows', fontsize=14, fontweight='bold', pad=15)
    
    ax.axvline(x=72, color='gray', linestyle='--', alpha=0.5)
    ax.text(72, 5, 'Phase transition (~72h)', rotation=90, va='bottom', fontsize=9, color='gray')
    
    ax.set_xlim(0, 168)
    ax.set_ylim(0, 130)  # Increased to prevent cutoff
    ax.legend(loc='upper right')
    
    plt.tight_layout(pad=2.0)  # Added padding
    plt.savefig(BASE_DIR / 'outputs' / 'figures' / 'figure5_sepsis_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: figure5_sepsis_timeline.png")

if __name__ == '__main__':
    print("Generating figures...")
    print("="*50)
    
    figure1_target_prioritization()
    figure2_compound_distribution()
    figure3_potency_by_target()
    figure4_pathway_heatmap()
    figure5_sepsis_timeline()
    
    print("="*50)
    print("All figures generated successfully!")
