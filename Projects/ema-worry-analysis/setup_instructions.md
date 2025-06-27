# EMA Worry Analysis - Setup Instructions

## Step-by-Step Setup Guide

### 1. Install Ollama and medGemma

#### Option A: Install Ollama (Recommended)
```bash
# Download and install Ollama from https://ollama.ai/download
# OR using Homebrew on macOS:
brew install ollama

# Pull the medGemma model
ollama pull medgemma-27b-text-it-mlx

# Start Ollama server (keep this running)
ollama serve
```

#### Option B: Alternative Models
If medGemma is not available, you can use other models:
```bash
# Try these alternatives:
ollama pull llama2
ollama pull mistral
ollama pull gemma
```

### 2. Set Up Python Environment

#### Option A: Using pip
```bash
cd /Users/kc/Projects/ema-worry-analysis
pip install -r requirements.txt
```

#### Option B: Using conda
```bash
cd /Users/kc/Projects/ema-worry-analysis
conda create -n ema-analysis python=3.9
conda activate ema-analysis
pip install -r requirements.txt
```

### 3. Verify Installation

#### Test Ollama Connection
```bash
# In a new terminal, test if Ollama is working:
curl http://localhost:11434/api/generate -d '{
  "model": "medgemma-27b-text-it-mlx",
  "prompt": "Hello, how are you?",
  "stream": false
}'
```

#### Test Python Dependencies
```bash
python -c "import pandas, numpy, matplotlib, seaborn, requests; print('All dependencies installed successfully!')"
```

### 4. Run the Analysis

#### Start Jupyter
```bash
cd /Users/kc/Projects/ema-worry-analysis
jupyter notebook
```

#### Open and Run the Notebook
1. In the Jupyter browser, click on `EMA_Worry_Analysis_medGemma.ipynb`
2. Run cells sequentially (Cell → Run All, or Shift+Enter for each cell)
3. The first run will test the medGemma connection
4. Then it will analyze the sample data

### 5. Using Your Own Data

#### Prepare Your Data
Your CSV file should have these columns:
- `participant_id`: Unique identifier for each participant
- `timestamp`: When the response was recorded
- `response_text`: The actual text response from participants

#### Update Configuration
In the notebook, modify the configuration cell:
```python
DATA_FILE_PATH = 'your_data_file.csv'  # Update this path
TEXT_COLUMN = 'your_text_column_name'  # Update column name
PARTICIPANT_COLUMN = 'your_participant_column'  # Update column name
TIMESTAMP_COLUMN = 'your_timestamp_column'  # Update column name
```

### 6. Expected Output

After running the analysis, you'll get:
- `ema_worry_analysis_results.csv`: Detailed results with worry scores
- `ema_worry_analysis_plots.png`: Visualizations
- `ema_worry_analysis_report.txt`: Summary report

## Common Issues and Solutions

### Issue 1: "Connection refused" to Ollama
**Solution**: Make sure Ollama is running: `ollama serve`

### Issue 2: "Model not found"
**Solution**: Pull the model: `ollama pull medgemma-27b-text-it-mlx`

### Issue 3: "Module not found" errors
**Solution**: Install missing packages: `pip install <package_name>`

### Issue 4: Jupyter doesn't start
**Solution**: Install Jupyter: `pip install jupyter notebook`

### Issue 5: medGemma gives unclear responses
**Solution**: The notebook handles this automatically and defaults to 0 (no worry)

## Performance Tips

- For large datasets (>1000 responses), increase `DELAY_BETWEEN_REQUESTS`
- Adjust `BATCH_SIZE` based on your system performance
- Consider processing data in chunks for very large datasets

## Model Alternatives

If medGemma is not available, modify the model configuration:
```python
MEDGEMMA_MODEL = 'llama2'  # or 'mistral', 'gemma', etc.
```

Note: Other models may require prompt adjustments for optimal worry detection.

## Getting Help

1. Check the troubleshooting section in the notebook
2. Ensure all prerequisites are installed
3. Verify your data format matches the expected structure
4. Test with the provided sample data first