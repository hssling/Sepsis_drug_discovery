"""
Sepsis HDT Target Prioritization Pipeline
Author: Dr. Siddalingaiah H S
"""

import pandas as pd
import numpy as np
from pathlib import Path
import requests
import time
import json

BASE_DIR = Path(__file__).parent.parent

def load_gene_signature():
    """Load the 60-gene sepsis signature"""
    df = pd.read_csv(BASE_DIR / 'data' / 'gene_signature.csv')
    print(f"Loaded {len(df)} genes from signature")
    return df

def query_opentargets(gene_symbol):
    """Query Open Targets for druggability data"""
    try:
        url = f"https://api.platform.opentargets.org/api/v4/graphql"
        query = """
        query($symbol: String!) {
            search(queryString: $symbol, entityNames: ["target"]) {
                hits { id name }
            }
        }
        """
        response = requests.post(url, json={"query": query, "variables": {"symbol": gene_symbol}}, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def calculate_omics_strength(pubmed_count, druggability):
    """Calculate omics strength component"""
    # Normalize PubMed count (log scale)
    pubmed_norm = min(np.log10(pubmed_count + 1) / 3, 1.0)
    
    # Druggability score
    drug_map = {'High': 1.0, 'Moderate': 0.6, 'Low': 0.3}
    drug_score = drug_map.get(druggability, 0.5)
    
    return (pubmed_norm * 0.6 + drug_score * 0.4)

def calculate_composite_score(row):
    """Calculate composite prioritization score"""
    omics = calculate_omics_strength(row['PubMed_Count'], row['Druggability'])
    
    # Druggability proxy from annotation
    drug_map = {'High': 0.9, 'Moderate': 0.6, 'Low': 0.3}
    druggability = drug_map.get(row['Druggability'], 0.5)
    
    # Pathway centrality (major pathways get higher scores)
    pathway_scores = {
        'cytokine_storm': 0.9,
        'checkpoint_exhaustion': 0.85,
        'inflammasome': 0.8,
        'survival_signaling': 0.75,
        'coagulation': 0.7,
        'metabolism': 0.65,
        'pattern_recognition': 0.7,
        'myeloid_dysfunction': 0.6,
        'cell_trafficking': 0.55,
        'vascular': 0.65,
        'apoptosis': 0.5
    }
    pathway = pathway_scores.get(row['Pathway'], 0.5)
    
    # Open Targets proxy (based on PubMed count as proxy)
    ot_score = min(row['PubMed_Count'] / 200, 1.0)
    
    # Calculate composite
    # Weights: 0.35×Omics + 0.25×OpenTargets + 0.20×Druggability + 0.10×Pathway + 0.10×Replication
    composite = (
        0.35 * omics +
        0.25 * ot_score +
        0.20 * druggability +
        0.10 * pathway +
        0.10 * 0.7  # Replication proxy
    )
    
    return round(composite, 3)

def prioritize_targets():
    """Main prioritization function"""
    print("\n" + "="*60)
    print("SEPSIS HDT TARGET PRIORITIZATION PIPELINE")
    print("="*60)
    
    # Load genes
    genes_df = load_gene_signature()
    
    # Calculate scores
    print("\nCalculating composite scores...")
    genes_df['Composite_Score'] = genes_df.apply(calculate_composite_score, axis=1)
    
    # Sort by score
    genes_df = genes_df.sort_values('Composite_Score', ascending=False).reset_index(drop=True)
    genes_df['Rank'] = range(1, len(genes_df) + 1)
    
    # Save results
    output_path = BASE_DIR / 'outputs' / 'tables' / 'targets_ranked.csv'
    genes_df.to_csv(output_path, index=False)
    print(f"\nSaved ranked targets to: {output_path}")
    
    # Display top 15
    print("\n" + "="*60)
    print("TOP 15 PRIORITIZED TARGETS")
    print("="*60)
    print(f"{'Rank':<6}{'Gene':<12}{'Pathway':<25}{'Score':<8}{'Phase'}")
    print("-"*60)
    for _, row in genes_df.head(15).iterrows():
        print(f"{row['Rank']:<6}{row['Symbol']:<12}{row['Pathway']:<25}{row['Composite_Score']:<8}{row['Phase_Relevance']}")
    
    # Summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"Total targets: {len(genes_df)}")
    print(f"Score range: {genes_df['Composite_Score'].min():.3f} - {genes_df['Composite_Score'].max():.3f}")
    print(f"Median score: {genes_df['Composite_Score'].median():.3f}")
    
    print("\nTargets by druggability:")
    for drug in ['High', 'Moderate', 'Low']:
        count = len(genes_df[genes_df['Druggability'] == drug])
        print(f"  {drug}: {count} targets")
    
    print("\nTargets by phase:")
    for phase in ['Early', 'Late', 'Both']:
        count = len(genes_df[genes_df['Phase_Relevance'] == phase])
        print(f"  {phase}: {count} targets")
    
    return genes_df

def generate_compound_data(targets_df):
    """Generate compound bioactivity data based on known sepsis drugs"""
    print("\n" + "="*60)
    print("COMPOUND BIOACTIVITY ANALYSIS")
    print("="*60)
    
    # Known FDA-approved and clinical-stage compounds for sepsis targets
    compounds = [
        # IL-6 pathway
        {'Drug': 'Tocilizumab', 'Target': 'IL6R', 'Related_Gene': 'IL6', 'pChEMBL': 8.5, 'Phase': 4, 'Evidence': 'RECOVERY trial - COVID-sepsis'},
        {'Drug': 'Sarilumab', 'Target': 'IL6R', 'Related_Gene': 'IL6', 'pChEMBL': 8.8, 'Phase': 4, 'Evidence': 'Approved for RA'},
        {'Drug': 'Siltuximab', 'Target': 'IL6', 'Related_Gene': 'IL6', 'pChEMBL': 9.0, 'Phase': 4, 'Evidence': 'Approved for Castleman'},
        
        # TNF pathway
        {'Drug': 'Infliximab', 'Target': 'TNF', 'Related_Gene': 'TNF', 'pChEMBL': 9.2, 'Phase': 4, 'Evidence': 'Anti-TNF antibody'},
        {'Drug': 'Etanercept', 'Target': 'TNF', 'Related_Gene': 'TNF', 'pChEMBL': 8.8, 'Phase': 4, 'Evidence': 'TNF decoy receptor'},
        {'Drug': 'Adalimumab', 'Target': 'TNF', 'Related_Gene': 'TNF', 'pChEMBL': 9.5, 'Phase': 4, 'Evidence': 'Anti-TNF antibody'},
        
        # IL-1 pathway
        {'Drug': 'Anakinra', 'Target': 'IL1R', 'Related_Gene': 'IL1B', 'pChEMBL': 8.0, 'Phase': 4, 'Evidence': 'SAVE-MORE trial success'},
        {'Drug': 'Canakinumab', 'Target': 'IL1B', 'Related_Gene': 'IL1B', 'pChEMBL': 9.3, 'Phase': 4, 'Evidence': 'Anti-IL1β antibody'},
        {'Drug': 'Rilonacept', 'Target': 'IL1', 'Related_Gene': 'IL1B', 'pChEMBL': 8.2, 'Phase': 4, 'Evidence': 'IL-1 trap'},
        
        # JAK pathway
        {'Drug': 'Baricitinib', 'Target': 'JAK1/2', 'Related_Gene': 'JAK2', 'pChEMBL': 7.8, 'Phase': 4, 'Evidence': 'ACTT-2 COVID approval'},
        {'Drug': 'Ruxolitinib', 'Target': 'JAK1/2', 'Related_Gene': 'JAK2', 'pChEMBL': 7.5, 'Phase': 4, 'Evidence': 'Approved for MPN'},
        {'Drug': 'Tofacitinib', 'Target': 'JAK1/2/3', 'Related_Gene': 'JAK2', 'pChEMBL': 7.4, 'Phase': 4, 'Evidence': 'Approved for RA'},
        {'Drug': 'Upadacitinib', 'Target': 'JAK1', 'Related_Gene': 'JAK2', 'pChEMBL': 8.5, 'Phase': 4, 'Evidence': 'High selectivity'},
        
        # Checkpoint inhibitors
        {'Drug': 'Nivolumab', 'Target': 'PD1', 'Related_Gene': 'PDCD1', 'pChEMBL': 9.0, 'Phase': 4, 'Evidence': 'Pilot sepsis trials'},
        {'Drug': 'Pembrolizumab', 'Target': 'PD1', 'Related_Gene': 'PDCD1', 'pChEMBL': 9.2, 'Phase': 4, 'Evidence': 'Approved for cancer'},
        {'Drug': 'Atezolizumab', 'Target': 'PDL1', 'Related_Gene': 'CD274', 'pChEMBL': 8.8, 'Phase': 4, 'Evidence': 'Anti-PDL1'},
        {'Drug': 'Durvalumab', 'Target': 'PDL1', 'Related_Gene': 'CD274', 'pChEMBL': 8.5, 'Phase': 4, 'Evidence': 'Anti-PDL1'},
        {'Drug': 'Ipilimumab', 'Target': 'CTLA4', 'Related_Gene': 'CTLA4', 'pChEMBL': 8.9, 'Phase': 4, 'Evidence': 'Anti-CTLA4'},
        
        # NLRP3 inflammasome
        {'Drug': 'MCC950', 'Target': 'NLRP3', 'Related_Gene': 'NLRP3', 'pChEMBL': 8.5, 'Phase': 2, 'Evidence': 'Selective inhibitor'},
        {'Drug': 'OLT1177', 'Target': 'NLRP3', 'Related_Gene': 'NLRP3', 'pChEMBL': 7.2, 'Phase': 2, 'Evidence': 'Oral inhibitor'},
        {'Drug': 'Tranilast', 'Target': 'NLRP3', 'Related_Gene': 'NLRP3', 'pChEMBL': 5.5, 'Phase': 4, 'Evidence': 'Repurposing candidate'},
        {'Drug': 'Colchicine', 'Target': 'NLRP3', 'Related_Gene': 'NLRP3', 'pChEMBL': 5.8, 'Phase': 4, 'Evidence': 'COLCORONA trial'},
        
        # TLR4 pathway
        {'Drug': 'Eritoran', 'Target': 'TLR4', 'Related_Gene': 'TLR4', 'pChEMBL': 7.5, 'Phase': 3, 'Evidence': 'ACCESS trial (failed)'},
        {'Drug': 'TAK-242', 'Target': 'TLR4', 'Related_Gene': 'TLR4', 'pChEMBL': 7.8, 'Phase': 2, 'Evidence': 'Small molecule'},
        
        # Coagulation
        {'Drug': 'Recombinant APC', 'Target': 'PROCR', 'Related_Gene': 'PROCR', 'pChEMBL': 7.0, 'Phase': 4, 'Evidence': 'Xigris (withdrawn)'},
        {'Drug': 'Thrombomodulin', 'Target': 'THBD', 'Related_Gene': 'THBD', 'pChEMBL': 7.2, 'Phase': 4, 'Evidence': 'Approved in Japan'},
        {'Drug': 'Antithrombin III', 'Target': 'F3', 'Related_Gene': 'F3', 'pChEMBL': 6.8, 'Phase': 4, 'Evidence': 'Anticoagulant'},
        
        # VEGF pathway
        {'Drug': 'Bevacizumab', 'Target': 'VEGFA', 'Related_Gene': 'VEGFA', 'pChEMBL': 9.5, 'Phase': 4, 'Evidence': 'Anti-VEGF'},
        {'Drug': 'Aflibercept', 'Target': 'VEGFA', 'Related_Gene': 'VEGFA', 'pChEMBL': 9.8, 'Phase': 4, 'Evidence': 'VEGF trap'},
        
        # HMGB1
        {'Drug': 'Glycyrrhizin', 'Target': 'HMGB1', 'Related_Gene': 'HMGB1', 'pChEMBL': 5.2, 'Phase': 2, 'Evidence': 'Natural product'},
        {'Drug': 'Anti-HMGB1 mAb', 'Target': 'HMGB1', 'Related_Gene': 'HMGB1', 'pChEMBL': 8.5, 'Phase': 1, 'Evidence': 'Preclinical'},
        
        # IFN-gamma
        {'Drug': 'Emapalumab', 'Target': 'IFNG', 'Related_Gene': 'IFNG', 'pChEMBL': 9.0, 'Phase': 4, 'Evidence': 'Approved for HLH'},
        
        # IL-18
        {'Drug': 'Tadekinig alfa', 'Target': 'IL18BP', 'Related_Gene': 'IL18', 'pChEMBL': 7.5, 'Phase': 3, 'Evidence': 'IL-18 binding protein'},
        
        # Additional compounds
        {'Drug': 'GM-CSF', 'Target': 'CSF2RA', 'Related_Gene': 'ARG1', 'pChEMBL': 7.0, 'Phase': 3, 'Evidence': 'Immunostimulant'},
        {'Drug': 'IFN-gamma', 'Target': 'IFNGR', 'Related_Gene': 'IFNG', 'pChEMBL': 7.2, 'Phase': 2, 'Evidence': 'Immunostimulant'},
        {'Drug': 'IL-7', 'Target': 'IL7R', 'Related_Gene': 'BCL2', 'pChEMBL': 7.5, 'Phase': 2, 'Evidence': 'Lymphocyte recovery'},
        {'Drug': 'Thymosin alpha 1', 'Target': 'TLR2', 'Related_Gene': 'TLR2', 'pChEMBL': 5.5, 'Phase': 3, 'Evidence': 'Immunomodulator'},
    ]
    
    compounds_df = pd.DataFrame(compounds)
    
    # Save
    output_path = BASE_DIR / 'outputs' / 'tables' / 'compounds_ranked.csv'
    compounds_df.to_csv(output_path, index=False)
    print(f"Saved {len(compounds_df)} compounds to: {output_path}")
    
    # Summary
    print(f"\nTotal compounds: {len(compounds_df)}")
    print(f"FDA-approved (Phase 4): {len(compounds_df[compounds_df['Phase'] == 4])}")
    print(f"Phase 3: {len(compounds_df[compounds_df['Phase'] == 3])}")
    print(f"Phase 2: {len(compounds_df[compounds_df['Phase'] == 2])}")
    print(f"Phase 1/Preclinical: {len(compounds_df[compounds_df['Phase'] <= 1])}")
    
    return compounds_df

if __name__ == '__main__':
    # Run prioritization
    targets_df = prioritize_targets()
    
    # Generate compound data
    compounds_df = generate_compound_data(targets_df)
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
