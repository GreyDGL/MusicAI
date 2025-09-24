#!/usr/bin/env python3
"""
Test script for MusicGen integration
"""

import sys
import torch
print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"MPS available: {torch.backends.mps.is_available()}")

# Test imports
try:
    from transformers import MusicgenForConditionalGeneration, AutoProcessor
    print("✓ Transformers imports successful")
except ImportError as e:
    print(f"✗ Failed to import transformers: {e}")
    sys.exit(1)

try:
    import scipy.io.wavfile
    print("✓ Scipy imports successful")
except ImportError as e:
    print(f"✗ Failed to import scipy: {e}")
    sys.exit(1)

print("\nAll dependencies installed correctly!")
print("\nNow you can:")
print("1. The web interface is running at http://localhost:8080")
print("2. Go to 'Generate' page to create music with MusicGen")
print("3. The first generation will download the model (~2.4GB for small model)")
print("4. Subsequent generations will be much faster as the model will be cached")