# MusicAI Installation and Usage Guide

## Quick Start (5 minutes)

### Requirements
- **OS**: macOS, Linux, or Windows (WSL)
- **Python**: 3.8+
- **RAM**: 8GB minimum
- **Storage**: 5GB free

### Installation
```bash
# Run the automated installer
chmod +x install.sh
./install.sh

# Start the application
./start.sh
```

Open http://localhost:8080 in your browser.

### Basic Usage

1. **Generate Music**: Click "Generate" → Enter prompt → Click "Generate Music"
   - Example: "A peaceful piano melody"
   - First run downloads model (~300MB-3GB)

2. **Evaluate Music**: Click "Evaluate" → Select file → Rate and submit

3. **Stop Application**: Run `./stop.sh`

---

## Common Issues

**Python not found**: Install Python 3.8+ from python.org

**ffmpeg missing**:
- Mac: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

**Out of memory**: Use "small" model size

**Port 8080 in use**: Kill existing process with `pkill -f "python app.py"`

---

## Advanced Usage

<details>
<summary><b>Command Line Interface</b></summary>

```bash
# Generate music via CLI
python musicgen_cli.py "A happy jazz piano solo"

# With options
python musicgen_cli.py "Epic orchestral music" --duration 15 --model medium
```
</details>

<details>
<summary><b>Prompt Examples</b></summary>

- **Classical**: "A dramatic Beethoven-style piano sonata"
- **Electronic**: "Ambient chillout track with soft synths, 90 BPM"
- **World Music**: "Japanese koto and shakuhachi duet, peaceful"
- **Jazz**: "Smooth jazz saxophone with piano accompaniment"
</details>

<details>
<summary><b>API Documentation</b></summary>

Generate music:
```bash
curl -X POST http://localhost:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A peaceful piano melody", "duration": 10}'
```

List files: `curl http://localhost:8080/api/music/list`
</details>

<details>
<summary><b>Manual Installation</b></summary>

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install PyTorch (Apple Silicon)
pip install torch==2.4.1 torchaudio==2.4.1

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_musicgen.txt

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```
</details>

<details>
<summary><b>Full Troubleshooting Guide</b></summary>

### Installation Issues
- **No torch module**: Reinstall PyTorch for your platform
- **Network timeout**: Install packages in smaller batches
- **Model download fails**: Check disk space and internet connection

### Runtime Issues
- **Generation slow**: Use "small" model
- **Memory error**: Close other apps, reduce duration
- **Port conflict**: `lsof -i :8080` then `kill -9 <PID>`

### Performance
- First generation downloads model (300MB-3GB)
- Apple Silicon uses MPS acceleration
- NVIDIA GPUs use CUDA automatically
</details>

---

**License**: Uses Meta's MusicGen (CC-BY-NC 4.0). Review before commercial use.