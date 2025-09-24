# MusicGen Integration Quick Start Guide

## ✅ Installation Complete!

The MusicGen integration is now fully set up and ready to use with your music evaluation system.

## 🚀 How to Use

### 1. Web Interface (Recommended)
The Flask application is running at: **http://localhost:8080**

1. Open your browser and go to http://localhost:8080
2. Click on **"Generate"** in the navigation menu
3. Enter a music description prompt (e.g., "A peaceful piano melody")
4. Select model size:
   - **Small** (300MB): Fast, good quality - downloads on first use
   - **Medium** (1.5GB): Balanced - better quality
   - **Large** (3.3GB): Best quality - slower generation
5. Click "Generate Music"
6. First generation will download the model (this takes a few minutes)
7. Once generated, go to "Evaluate" to listen and evaluate the music

### 2. Command Line Interface
You can also generate music directly from the terminal:

```bash
# Basic usage
python musicgen_cli.py "A happy jazz piano solo"

# With options
python musicgen_cli.py "Epic orchestral battle music" --duration 15 --model medium

# List available models
python musicgen_cli.py --list-models
```

## 📊 Features

### What's Working:
- ✅ **Real MusicGen Integration**: Uses Meta's actual MusicGen model
- ✅ **Multiple Model Sizes**: Small, Medium, Large, and Melody models
- ✅ **Web Interface**: User-friendly interface for generation and evaluation
- ✅ **Evaluation System**: Structured evaluation with your expert criteria
- ✅ **Music Library**: Automatic scanning and management
- ✅ **Dashboard**: Statistics and overview of all generated music
- ✅ **Export**: Export all evaluation data as JSON

### Generation Parameters:
- **Duration**: 1-30 seconds
- **Temperature**: 0.1-2.0 (higher = more creative)
- **Guidance Scale**: 1.0-5.0 (higher = follows prompt more closely)
- **Model Size**: Small/Medium/Large/Melody

## 🎵 Example Prompts

Try these prompts to test different styles:

1. **Classical**: "A dramatic Beethoven-style piano sonata"
2. **Electronic**: "Upbeat electronic dance music with heavy bass, 128 BPM"
3. **Jazz**: "Smooth jazz saxophone with piano accompaniment"
4. **World Music**: "Japanese koto and shakuhachi duet, peaceful"
5. **Ambient**: "Ethereal ambient soundscape with nature sounds"
6. **Rock**: "90s rock song with electric guitars and drums"
7. **Folk**: "Celtic folk music with fiddle and bodhrán drum"
8. **Orchestral**: "Epic cinematic orchestra with strings and brass"

## ⚠️ Important Notes

1. **First Generation**: The first time you generate music, the model will be downloaded (~2.4GB for small model). This is a one-time download.

2. **Performance**: 
   - On Apple Silicon Macs, the model will use MPS (Metal Performance Shaders) for acceleration
   - Generation takes 10-60 seconds depending on duration and model size
   - Small model is recommended for testing

3. **Memory Usage**: 
   - Small model: ~2GB RAM
   - Medium model: ~6GB RAM
   - Large model: ~12GB RAM

## 🔧 Troubleshooting

### If generation fails:
1. Check that you have enough disk space for model download
2. Check RAM availability
3. Try using the small model first
4. Check the terminal for error messages

### To restart the application:
```bash
pkill -f "python app.py"
python app.py
```

## 📁 File Locations

- Generated music: `music/` folder
- Database: `database.db`
- Logs: Terminal output
- Model cache: `~/.cache/huggingface/hub/`

## 🎯 Next Steps

1. Generate your first music piece
2. Evaluate it using the structured criteria
3. Compare different prompts and parameters
4. Export evaluation data for analysis
5. Build a library of evaluated AI-generated music

Enjoy creating and evaluating AI-generated music!