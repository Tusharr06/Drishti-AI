# Drishti AI - Vision Intelligence

An advanced image analysis application powered by Ollama Vision Language Models with a modern, feature-rich Streamlit interface. The name "Drishti" (दृष्टि) comes from Sanskrit, meaning "vision" or "sight" - perfectly representing our AI vision analysis platform.

## ✨ Features

### 🖼️ Single Image Analysis

- **Multiple Model Support**: Choose from LLaVA, BakLLaVA, MiniCPM-V, Moondream, and more
- **Real-time Image Enhancement**: Adjust brightness, contrast, saturation, and blur
- **Custom Prompts**: Use predefined templates or create custom analysis prompts
- **Detailed Results**: Get comprehensive analysis with processing time and token usage
- **Export Options**: Download results as text or JSON files

### 📊 Batch Processing

- **Multiple Image Upload**: Process up to 20 images simultaneously
- **Progress Tracking**: Real-time progress bar and status updates
- **Batch Export**: Export all results in a single JSON file
- **Error Handling**: Continue processing even if individual images fail

### 🔍 Compare Images

- **Side-by-Side Analysis**: Compare 2-4 images simultaneously
- **Individual Analysis**: Get detailed analysis for each image
- **Comparative Summary**: AI-generated comparison highlighting similarities and differences
- **Export Comparisons**: Save comparison results for future reference

### 📜 Session History

- **Analysis Tracking**: Keep track of all analyses in your session
- **Performance Metrics**: Monitor processing times and efficiency
- **Export History**: Download complete session history as ZIP file
- **Search & Filter**: Easy access to previous analyses

### 🛠️ Advanced Settings

- **Model Configuration**: Fine-tune temperature, max tokens, and other parameters
- **Image Enhancement**: Real-time image processing with multiple filters
- **Prompt Templates**: Pre-built prompts for different use cases
- **Performance Monitoring**: Track processing times and model performance

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.com) installed and running
- At least one vision model pulled (e.g., `ollama pull llava:7b`)

### Setup Steps

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Install and configure Ollama**:

   ```bash
   # Install Ollama (visit https://ollama.com for platform-specific instructions)

   # Pull vision models
   ollama pull llava:7b
   ollama pull llava:13b
   ollama pull llava-phi3
   ollama pull bakllava
   ollama pull minicpm-v
   ollama pull moondream
   ```

3. **Run the application**:

   ```bash
   streamlit run src/app/main.py
   ```

4. **Access the app**: Open your browser and go to `http://localhost:8501`

## Configuration

### Environment Variables

- `OLLAMA_HOST`: Ollama server host (default: localhost)
- `OLLAMA_PORT`: Ollama server port (default: 11434)

### Model Information

| Model          | Size  | Speed  | Accuracy   | Best For                                   |
| -------------- | ----- | ------ | ---------- | ------------------------------------------ |
| **moondream**  | 1.86B | ⚡⚡⚡ | ⭐⭐       | Quick analysis, basic descriptions         |
| **minicpm-v**  | 2.8B  | ⚡⚡⚡ | ⭐⭐⭐     | Multilingual content, efficient processing |
| **llava-phi3** | 3.8B  | ⚡⚡   | ⭐⭐⭐     | Balanced performance, resource-efficient   |
| **llava:7b**   | 7B    | ⚡⚡   | ⭐⭐⭐⭐   | General purpose, good balance              |
| **bakllava**   | 7B    | ⚡⚡   | ⭐⭐⭐⭐   | Visual reasoning, scene understanding      |
| **llava:13b**  | 13B   | ⚡     | ⭐⭐⭐⭐⭐ | Detailed analysis, high accuracy           |
| **llava:34b**  | 34B   | ⚡     | ⭐⭐⭐⭐⭐ | Complex analysis, highest accuracy         |

## 📝 Usage Examples

### Basic Image Analysis

1. Upload an image using the file uploader
2. Select your preferred model and adjust settings
3. Choose or write a custom prompt
4. Click "Analyze Image" to get results

### Batch Processing

1. Go to the "Batch Processing" tab
2. Upload multiple images (up to 20)
3. Enter a batch processing prompt
4. Configure model settings
5. Click "Process All Images"

### Image Comparison

1. Navigate to the "Compare Images" tab
2. Upload 2-4 images for comparison
3. Enter a comparison prompt
4. Review individual analyses and comparative summary

### Prompt Templates

The application includes several built-in prompt templates:

- **General Description**: Comprehensive image description
- **Technical Analysis**: Focus on technical aspects and composition
- **Creative Writing**: Generate creative narratives
- **Accessibility**: Detailed descriptions for visually impaired users
- **Educational**: Extract educational insights
- **Marketing**: Analyze from branding perspective
- **Art Critique**: Artistic analysis and critique
- **OCR**: Extract text from images
- **Object Detection**: Identify objects and items
- **Scene Understanding**: Analyze context and setting

## ️ Advanced Features

### Image Enhancement

- **Brightness**: Adjust image brightness (0.5x - 2.0x)
- **Contrast**: Modify contrast levels (0.5x - 2.0x)
- **Saturation**: Control color saturation (0.0x - 2.0x)
- **Blur**: Apply Gaussian blur (0-5 pixels)

### Export Options

- **Text Format**: Simple text file with analysis results
- **JSON Format**: Structured data with metadata
- **ZIP Archive**: Complete session history with all analyses
- **Batch Results**: Consolidated results from batch processing

### Performance Monitoring

- **Processing Time**: Track analysis duration for each image
- **Session Statistics**: Monitor total processed images and time
- **Model Comparison**: Compare performance across different models

## 🎯 Use Cases

### Content Creation

- Generate image descriptions for social media
- Create alt-text for web accessibility
- Analyze visual content for marketing campaigns

### Education & Research

- Analyze historical photographs
- Study artistic techniques and compositions
- Extract information from diagrams and charts

### Business Applications

- Product image analysis for e-commerce
- Quality control through visual inspection
- Brand monitoring and analysis

### Accessibility

- Generate detailed descriptions for visually impaired users
- Create comprehensive alt-text for websites
- Analyze visual content for accessibility compliance

## 🔍 Troubleshooting

### Common Issues

**"Model not available" error**:

```bash
ollama pull <model-name>
```

**Ollama connection failed**:

- Ensure Ollama is running: `ollama serve`
- Check if the correct port is used (default: 11434)

**Out of memory errors**:

- Try smaller models (moondream, llava-phi3)
- Reduce max_tokens parameter
- Process images individually instead of batch

**Slow processing**:

- Use faster models for quick analysis
- Reduce image size before upload
- Lower temperature and max_tokens settings

## 🤝 Contributing

We welcome contributions! Please feel free to:

- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Ollama](https://ollama.com) for the amazing local LLM platform
- [Streamlit](https://streamlit.io) for the excellent web app framework
- The open-source vision language model communities
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information
4. Join our community discussions

---

**Built with ❤️ using Streamlit and Ollama**
