# Detailed Methodology

## 1. Study Design

This computational, in silico study employed a systems biology approach to identify phase-specific host-directed therapy targets for sepsis. The analysis integrated:

1. Curated transcriptomic signatures from multiple GEO datasets
2. Druggability assessments from Open Targets Platform
3. Compound bioactivity data from ChEMBL database

## 2. Gene Signature Curation

### 2.1 Data Sources

| GEO ID | Description | Samples | Platform | Reference |
|--------|-------------|---------|----------|-----------|
| GSE185263 | Sepsis vs SIRS | 479 | RNA-seq | Baghela 2022 |
| GSE65682 | MARS cohort | 802 | Microarray | Scicluna 2017 |
| GSE134347 | Septic shock | 51 | RNA-seq | Davenport 2016 |
| GSE69528 | Pediatric sepsis | 162 | Microarray | Wong 2015 |

### 2.2 Gene Selection Criteria

Genes were included if they met:
- Consistent differential expression (|log₂FC| ≥ 1.0)
- Statistical significance (FDR < 0.05)
- Biological relevance to sepsis immunopathology

### 2.3 Phase Annotation

Each gene was classified based on temporal expression:
- **Early (0-72h):** Peak expression during hyperinflammation
- **Late (>72h):** Peak expression during immunosuppression
- **Both:** Sustained dysregulation across phases

## 3. Target Prioritization Algorithm

### 3.1 Scoring Formula

```
Composite Score = Σ(wᵢ × Sᵢ)
```

Where:
- w₁ = 0.35 (Omics strength)
- w₂ = 0.25 (Open Targets evidence)
- w₃ = 0.20 (Druggability proxy)
- w₄ = 0.10 (Pathway centrality)
- w₅ = 0.10 (Replication)

### 3.2 Component Definitions

**Omics Strength (S₁):**
- Normalized PubMed count (log scale)
- Combined with druggability annotation

**Open Targets Evidence (S₂):**
- Aggregate score from platform
- Includes genetic, drug, and pathway evidence

**Druggability Proxy (S₃):**
- High = 0.9 (approved drugs exist)
- Moderate = 0.6 (clinical-stage drugs)
- Low = 0.3 (preclinical only)

**Pathway Centrality (S₄):**
- Weighted by pathway importance in sepsis
- Cytokine storm pathway: 0.9
- Checkpoint exhaustion: 0.85
- Inflammasome: 0.8

**Replication (S₅):**
- Evidence across multiple datasets
- Fixed at 0.7 for curated signature

## 4. Compound Mining

### 4.1 ChEMBL Query

For each target, we queried ChEMBL v33 for:
- IC50, Ki, Kd values
- pChEMBL ≥ 6.0 (≤1 µM potency)
- Confidence score ≥ 7

### 4.2 Clinical Phase Assignment

| Phase | Definition |
|-------|------------|
| 4 | FDA approved |
| 3 | Phase III trials |
| 2 | Phase II trials |
| 1 | Phase I / Preclinical |

## 5. Reproducibility

### 5.1 Software Versions

- Python: 3.12
- pandas: 2.0+
- matplotlib: 3.7+
- seaborn: 0.12+

### 5.2 Running the Pipeline

```bash
# Clone repository
git clone https://github.com/hssling/Sepsis_drug_discovery.git

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python scripts/run_pipeline.py

# Run tests
pytest tests/ -v
```

### 5.3 Expected Outputs

- `outputs/tables/targets_ranked.csv`: 60 ranked targets
- `outputs/tables/compounds_ranked.csv`: 37 compounds
- `outputs/figures/`: 5 publication-quality figures
