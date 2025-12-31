# Reproducibility Guide

## System Requirements

- Python 3.10+ (tested on 3.10, 3.11, 3.12)
- 4GB RAM minimum
- 1GB disk space

## Step-by-Step Reproduction

### 1. Clone Repository

```bash
git clone https://github.com/hssling/Sepsis_drug_discovery.git
cd Sepsis_drug_discovery
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import pandas; import matplotlib; print('Dependencies OK')"
```

### 5. Run Pipeline

```bash
python scripts/run_pipeline.py
```

Expected output:
```
============================================================
SEPSIS HDT TARGET PRIORITIZATION PIPELINE
============================================================
Loaded 60 genes from signature
Calculating composite scores...

============================================================
TOP 15 PRIORITIZED TARGETS
============================================================
Rank  Gene        Pathway                   Score   Phase
------------------------------------------------------------
1     IL6         cytokine_storm            0.520   Early
2     TNF         cytokine_storm            0.485   Early
3     TLR4        pattern_recognition       0.478   Early
...
```

### 6. Generate Figures

```bash
python scripts/generate_figures.py
```

Generates 5 PNG files in `outputs/figures/`

### 7. Run Tests

```bash
pytest tests/ -v
```

All tests should pass (18/18).

## Output Verification

### Checksum Verification

```bash
# Windows
certutil -hashfile outputs/tables/targets_ranked.csv MD5

# Linux/Mac
md5sum outputs/tables/targets_ranked.csv
```

### Expected File Sizes

| File | Size | Format |
|------|------|--------|
| targets_ranked.csv | ~4.5 KB | CSV |
| compounds_ranked.csv | ~1.8 KB | CSV |
| figure1*.png | ~250 KB | PNG |
| figure2*.png | ~250 KB | PNG |
| figure3*.png | ~220 KB | PNG |
| figure4*.png | ~435 KB | PNG |
| figure5*.png | ~350 KB | PNG |

## Known Issues

1. **Network errors:** API calls may timeout; retry after 30 seconds
2. **Memory:** Large GEO datasets may require 8GB RAM
3. **Windows paths:** Use forward slashes or raw strings

## Support

For issues, contact: hssling@yahoo.com
