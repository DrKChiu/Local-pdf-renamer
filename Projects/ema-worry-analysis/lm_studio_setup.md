# LM Studio Setup for EMA Worry Analysis

## Step-by-Step LM Studio Setup

### 1. Install and Setup LM Studio

#### Download LM Studio
1. Go to https://lmstudio.ai/
2. Download LM Studio for your operating system
3. Install and launch the application

#### Load medGemma Model
1. In LM Studio, go to the "Discover" tab
2. Search for "medgemma-27b-text-it-mlx"
3. Download the model (this may take a while - it's a large file)
4. Once downloaded, go to the "Chat" tab
5. Select "medgemma-27b-text-it-mlx" from the model dropdown

### 2. Start the Local Server

#### Enable API Server
1. In LM Studio, click on the "Local Server" tab (left sidebar)
2. Select your medgemma model from the dropdown
3. Click "Start Server"
4. The server should start on `http://localhost:1234`
5. Keep LM Studio running with the server active

#### Verify Server is Running
Test the API endpoint:
```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "medgemma-27b-text-it-mlx",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.1,
    "max_tokens": 50
  }'
```

### 3. Install Python Dependencies

```bash
cd /Users/kc/Projects/ema-worry-analysis
pip install -r requirements.txt
```

### 4. Run the Analysis

#### Start Jupyter
```bash
cd /Users/kc/Projects/ema-worry-analysis
jupyter notebook
```

#### Open and Run the Notebook
1. In Jupyter, click on `EMA_Worry_Analysis_medGemma.ipynb`
2. Run all cells sequentially
3. The notebook will first test the LM Studio connection
4. Then analyze the sample EMA data

### 5. Expected Workflow

1. **LM Studio Setup**: Load medgemma model and start local server
2. **Connection Test**: Notebook tests API connection
3. **Data Analysis**: Process EMA text responses for worry detection
4. **Results**: Generate visualizations and export analysis results

## LM Studio Configuration Notes

### Model Selection
- Use `medgemma-27b-text-it-mlx` for best medical text analysis
- Alternative models: `llama-2-7b-chat` or `mistral-7b-instruct`

### Server Settings
- **Port**: Default 1234 (update notebook if different)
- **Context Length**: Set to at least 4096 tokens
- **Temperature**: 0.1 (for consistent results)

### Performance Tips
- **GPU Acceleration**: Enable if available for faster processing
- **Batch Size**: Reduce if experiencing memory issues
- **Delay**: Increase `DELAY_BETWEEN_REQUESTS` if getting rate limit errors

## Troubleshooting

### Common Issues

#### "Connection refused" Error
- **Cause**: LM Studio server not running
- **Solution**: Start the Local Server in LM Studio

#### "Model not found" Error
- **Cause**: Model name mismatch
- **Solution**: Check the exact model name in LM Studio and update notebook

#### Slow Response Times
- **Cause**: Large model, limited resources
- **Solution**: 
  - Close other applications
  - Increase `DELAY_BETWEEN_REQUESTS` in notebook
  - Consider using a smaller model

#### Memory Issues
- **Cause**: Model too large for available RAM
- **Solution**:
  - Use quantized version of the model
  - Reduce context length in LM Studio
  - Process data in smaller batches

### API Endpoint Verification
Ensure LM Studio is properly configured:
1. Local Server tab shows "Server Running"
2. Model is loaded and selected
3. Port is 1234 (or update notebook configuration)

### Model Alternatives
If medgemma is not available:
```python
# In notebook configuration cell, try:
LM_STUDIO_MODEL = 'llama-2-7b-chat'
# or
LM_STUDIO_MODEL = 'mistral-7b-instruct-v0.1'
```

## Performance Optimization

### For Large Datasets
- Set `BATCH_SIZE = 5` (smaller batches)
- Set `DELAY_BETWEEN_REQUESTS = 3` (longer delays)
- Process data in chunks if very large

### For Better Accuracy
- Use the full medgemma model (not quantized)
- Set temperature to 0.1 for consistent results
- Validate results on a sample of responses

## Next Steps

Once setup is complete:
1. Test with the provided sample data
2. Replace with your own m-path EMA export
3. Review and validate worry classification results
4. Adjust prompts if needed for better accuracy