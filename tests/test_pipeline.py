"""
Unit tests for Sepsis HDT Pipeline
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestGeneSignature:
    """Test gene signature loading and validation"""
    
    def test_gene_signature_exists(self):
        """Verify gene signature file exists"""
        path = Path(__file__).parent.parent / 'data' / 'gene_signature.csv'
        assert path.exists(), "Gene signature file not found"
    
    def test_gene_signature_columns(self):
        """Verify required columns exist"""
        path = Path(__file__).parent.parent / 'data' / 'gene_signature.csv'
        df = pd.read_csv(path)
        required_cols = ['Gene', 'Symbol', 'Pathway', 'Phase_Relevance', 'Druggability']
        for col in required_cols:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_gene_signature_count(self):
        """Verify 60 genes in signature"""
        path = Path(__file__).parent.parent / 'data' / 'gene_signature.csv'
        df = pd.read_csv(path)
        assert len(df) == 60, f"Expected 60 genes, got {len(df)}"
    
    def test_valid_phases(self):
        """Verify phase values are valid"""
        path = Path(__file__).parent.parent / 'data' / 'gene_signature.csv'
        df = pd.read_csv(path)
        valid_phases = {'Early', 'Late', 'Both'}
        for phase in df['Phase_Relevance'].unique():
            assert phase in valid_phases, f"Invalid phase: {phase}"


class TestPipelineOutputs:
    """Test pipeline output files"""
    
    def test_targets_ranked_exists(self):
        """Verify targets output exists"""
        path = Path(__file__).parent.parent / 'outputs' / 'tables' / 'targets_ranked.csv'
        assert path.exists(), "targets_ranked.csv not found"
    
    def test_compounds_ranked_exists(self):
        """Verify compounds output exists"""
        path = Path(__file__).parent.parent / 'outputs' / 'tables' / 'compounds_ranked.csv'
        assert path.exists(), "compounds_ranked.csv not found"
    
    def test_targets_have_scores(self):
        """Verify all targets have composite scores"""
        path = Path(__file__).parent.parent / 'outputs' / 'tables' / 'targets_ranked.csv'
        df = pd.read_csv(path)
        assert 'Composite_Score' in df.columns
        assert df['Composite_Score'].notna().all(), "Some targets missing scores"
    
    def test_scores_in_valid_range(self):
        """Verify scores are between 0 and 1"""
        path = Path(__file__).parent.parent / 'outputs' / 'tables' / 'targets_ranked.csv'
        df = pd.read_csv(path)
        assert (df['Composite_Score'] >= 0).all(), "Scores below 0 found"
        assert (df['Composite_Score'] <= 1).all(), "Scores above 1 found"


class TestFigures:
    """Test figure generation"""
    
    @pytest.mark.parametrize("figure_name", [
        "figure1_target_prioritization.png",
        "figure2_compound_distribution.png",
        "figure3_target_potency.png",
        "figure4_pathway_heatmap.png",
        "figure5_sepsis_timeline.png",
    ])
    def test_figure_exists(self, figure_name):
        """Verify each figure was generated"""
        path = Path(__file__).parent.parent / 'outputs' / 'figures' / figure_name
        assert path.exists(), f"Figure not found: {figure_name}"
    
    @pytest.mark.parametrize("figure_name", [
        "figure1_target_prioritization.png",
        "figure2_compound_distribution.png",
        "figure3_target_potency.png",
        "figure4_pathway_heatmap.png",
        "figure5_sepsis_timeline.png",
    ])
    def test_figure_not_empty(self, figure_name):
        """Verify figures have content"""
        path = Path(__file__).parent.parent / 'outputs' / 'figures' / figure_name
        assert path.stat().st_size > 10000, f"Figure seems too small: {figure_name}"


class TestScoring:
    """Test scoring algorithm"""
    
    def test_il6_top_ranked(self):
        """IL-6 should be among top 5 targets"""
        path = Path(__file__).parent.parent / 'outputs' / 'tables' / 'targets_ranked.csv'
        df = pd.read_csv(path)
        top5_genes = df.head(5)['Symbol'].tolist()
        assert 'IL6' in top5_genes, "IL-6 should be top-ranked given literature"
    
    def test_phase_distribution(self):
        """Verify phase distribution is reasonable"""
        path = Path(__file__).parent.parent / 'outputs' / 'tables' / 'targets_ranked.csv'
        df = pd.read_csv(path)
        phase_counts = df['Phase_Relevance'].value_counts()
        assert len(phase_counts) >= 2, "Should have multiple phase categories"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
