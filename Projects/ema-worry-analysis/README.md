# EMA Worry Analysis Project

© 2024 [Your Name]. All rights reserved.

This project analyzes Ecological Momentary Assessment (EMA) text data to detect worry patterns using medGemma AI model.

## Copyright Notice
This software is protected by copyright. See [COPYRIGHT.md](COPYRIGHT.md) for full details.
For commercial use or licensing inquiries, contact: [Your Email]

## Citation
If you use this framework in your research, please cite it:
```bibtex
@software{ema_worry_analysis_2024,
  author = {[Your Name]},
  title = {EMA Worry Analysis Framework},
  year = {2024},
  url = {[Your GitHub Repository URL]}
}
```

## Project Structure
```
ema-worry-analysis/
├── README.md                           # This file
├── EMA_Worry_Analysis_medGemma.ipynb  # Main analysis notebook
├── sample_mpath_ema_data.csv          # Sample EMA data
├── requirements.txt                   # Python dependencies
└── setup_instructions.md              # Detailed setup guide
```

## Quick Start

### 1. Prerequisites
- Python 3.8+
- Jupyter Notebook or JupyterLab
- LM Studio (for running medGemma locally)

### 2. Setup LM Studio with medGemma
1. Download LM Studio from https://lmstudio.ai/
2. Install and launch LM Studio
3. Download `medgemma-27b-text-it-mlx` model
4. Go to "Local Server" tab and start the server
5. Keep LM Studio running with the server active

See `lm_studio_setup.md` for detailed instructions.

### 3. Install Python Dependencies
```bash
cd /Users/kc/Projects/ema-worry-analysis
pip install -r requirements.txt
```

### 4. Run the Analysis
```bash
# Start Jupyter
jupyter notebook

# Open EMA_Worry_Analysis_medGemma.ipynb
# Run all cells sequentially
```

## What This Project Does

1. **Data Loading**: Imports m-path EMA CSV exports
2. **Text Analysis**: Uses medGemma to classify worry presence (1) or absence (0)
3. **Visualization**: Creates charts showing worry patterns
4. **Export**: Saves results to CSV and generates reports

## Sample Output

The analysis produces:
- Detailed CSV with worry scores for each response
- Statistical summary by participant
- Visualizations of worry patterns
- Text-based summary report

## Customization

Update the configuration section in the notebook:
- `DATA_FILE_PATH`: Path to your EMA data file
- `LM_STUDIO_API_URL`: LM Studio API endpoint (default: http://localhost:1234/v1/chat/completions)
- `LM_STUDIO_MODEL`: Model name in LM Studio
- Column names to match your data format

## Troubleshooting

See the troubleshooting section in the notebook for common issues and solutions.