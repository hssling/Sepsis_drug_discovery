# Sepsis Host-Directed Therapy Drug Discovery Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo-blue)](https://zenodo.org/)

## 🎯 Overview

An integrated multi-omics and chemoinformatics pipeline for identifying **phase-specific host-directed therapy (HDT) targets** in sepsis. This pipeline addresses the critical challenge of sepsis treatment by stratifying therapeutic targets based on the biphasic immune response.

### Why Sepsis HDT?

| Statistic | Value | Significance |
|-----------|-------|--------------|
| Annual cases | 48.9 million | Leading cause of hospital death |
| Annual deaths | 11 million | 20% of all global deaths |
| Failed trials | 100+ | No new drugs since 1960s |
| Treatment gap | Critical | Unmet medical need |

### The Sepsis Immune Paradox

Sepsis involves a **biphasic immune response** that explains past trial failures:

```
Time:     0h -------- 24h -------- 72h -------- 168h
          |           |            |            |
Phase:    |<-- EARLY (Hyperinflammation) -->|<-- LATE (Immunosuppression) -->|
          |           |            |            |
Targets:  |  IL-6, NLRP3, TNF     |   PD-1, TIM-3, LAG-3              |
          |  TLR4, IL-1β          |   GM-CSF, IL-7                     |
```

## 🔬 Key Findings

### Top Priority Targets

| Rank | Target | Score | Phase | Therapeutic Approach |
|------|--------|-------|-------|---------------------|
| 1 | **IL-6** | 0.520 | Early | Tocilizumab (RECOVERY trial ✓) |
| 2 | TNF | 0.485 | Early | Anti-TNF (phase mismatch lessons) |
| 3 | **TLR4** | 0.478 | Early | TAK-242 (Phase II) |
| 4 | **PD-1** | 0.452 | Late | Nivolumab (pilot success) |
| 5 | **NLRP3** | 0.423 | Early | MCC950, Colchicine |

### FDA-Approved Repurposing Candidates

| Drug | Target | Evidence Level | Indication |
|------|--------|----------------|------------|
| **Tocilizumab** | IL-6R | Phase IV (COVID) | Early sepsis |
| **Baricitinib** | JAK1/2 | FDA approved | Both phases |
| **Anakinra** | IL-1R | SAVE-MORE ✓ | Early sepsis |
| **Colchicine** | NLRP3 | COLCORONA ✓ | Early sepsis |
| **Nivolumab** | PD-1 | Phase 1b | Late sepsis |

## 📁 Project Structure

```
Sepsis_HDT_Pipeline/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Continuous integration
│       └── lint.yml            # Code linting
├── config/
│   └── sepsis_config.yaml      # Pipeline configuration
├── data/
│   ├── gene_signature.csv      # 60-gene sepsis signature
│   └── geo_datasets/           # GEO dataset references
├── docs/
│   ├── METHODOLOGY.md          # Detailed methods
│   ├── REPRODUCIBILITY.md      # Reproduction guide
│   └── API.md                  # API documentation
├── manuscripts/
│   ├── Manuscript_Sepsis_HDT.docx
│   ├── Supplementary_Materials.docx
│   └── CoverLetter_IJCCM.md
├── outputs/
│   ├── figures/                # Publication-quality figures
│   └── tables/                 # CSV output tables
├── scripts/
│   ├── run_pipeline.py         # Main pipeline
│   ├── generate_figures.py     # Figure generation
│   ├── generate_manuscript.py  # DOCX generation
│   └── generate_supplementary.py
├── tests/
│   ├── test_pipeline.py
│   └── test_scoring.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
└── pyproject.toml
```

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/hssling/Sepsis_drug_discovery.git
cd Sepsis_drug_discovery

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Pipeline

```bash
# Full pipeline (targets + compounds)
python scripts/run_pipeline.py

# Generate figures only
python scripts/generate_figures.py

# Generate manuscript
python scripts/generate_manuscript.py

# Generate supplementary materials
python scripts/generate_supplementary.py
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html
```

## 📊 Methodology

### Data Sources

| Database | Version | Usage |
|----------|---------|-------|
| GEO | Dec 2024 | Transcriptomic signatures |
| ChEMBL | v33 | Compound bioactivity |
| Open Targets | 24.09 | Druggability assessment |
| MyGene.info | v3 | Gene-protein mapping |

### Key GEO Datasets

| ID | Description | Samples | Platform |
|----|-------------|---------|----------|
| GSE185263 | Sepsis vs SIRS | 479 | RNA-seq |
| GSE65682 | MARS cohort | 802 | Microarray |
| GSE134347 | Septic shock severity | 51 | RNA-seq |
| GSE69528 | Pediatric sepsis | 162 | Microarray |

### Scoring Algorithm

```
Composite Score = 0.35 × Omics_Evidence 
                + 0.25 × OpenTargets_Score
                + 0.20 × Druggability
                + 0.10 × Pathway_Centrality
                + 0.10 × Replication
```

## 📈 Outputs

### Tables
- `targets_ranked.csv`: 60 prioritized host targets
- `compounds_ranked.csv`: 37 clinically advanced compounds

### Figures
1. **Figure 1**: Target prioritization (phase-colored)
2. **Figure 2**: Compound distribution by clinical phase
3. **Figure 3**: Target potency profile
4. **Figure 4**: Pathway heatmap
5. **Figure 5**: Sepsis immune timeline with HDT windows

## 📝 Citation

If you use this pipeline, please cite:

```bibtex
@article{siddalingaiah2024sepsis,
  title={Phase-Specific Host-Directed Therapy Targets in Sepsis: An Integrated 
         Multi-omics and Chemoinformatics Pipeline},
  author={Siddalingaiah, H S},
  journal={Indian Journal of Critical Care Medicine},
  year={2024},
  note={Submitted}
}
```

## 👤 Author

**Dr. Siddalingaiah H S**  
Professor, Department of Community Medicine  
Shridevi Institute of Medical Sciences and Research Hospital  
Tumkur – 572106, Karnataka, India

- 📧 Email: hssling@yahoo.com
- 📞 Phone: +91-8941087719
- 🆔 ORCID: [0000-0002-4771-8285](https://orcid.org/0000-0002-4771-8285)
- 🏥 Institution: [SIMS Tumkur](https://simstumkur.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ChEMBL Database** (EMBL-EBI) for compound bioactivity data
- **Open Targets Platform** for druggability assessments
- **GEO Database** (NCBI) for transcriptomic data
- **MARS Consortium** for sepsis transcriptomic resources
- **RECOVERY Trial Investigators** for clinical validation data

## 📚 Related Projects

- [Tuberculosis HDT Pipeline](https://github.com/hssling/TB_HDT_Pipeline)
- [Leprosy Drug Discovery](https://github.com/hssling/Leprosy_drug_discovery)

---

**⚠️ Disclaimer:** This is a computational study for research purposes. Clinical application of identified targets requires prospective validation through randomized controlled trials.
