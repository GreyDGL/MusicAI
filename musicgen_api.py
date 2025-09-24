"""
MusicGen API Integration Module
This module provides integration with Meta's MusicGen model for music generation.
"""

import os
import time
import torch
import scipy
import numpy as np
from datetime import datetime
from transformers import MusicgenForConditionalGeneration, AutoProcessor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to cache the model
_cached_model = None
_cached_processor = None

def load_musicgen_model(model_size='small', device=None):
    """
    Load and cache the MusicGen model.
    
    Args:
        model_size (str): Model size - 'small', 'medium', or 'large'
        device (str): Device to use ('cuda', 'cpu', or None for auto-detect)
    
    Returns:
        tuple: (model, processor, device)
    """
    global _cached_model, _cached_processor
    
    if _cached_model is None or _cached_processor is None:
        logger.info(f"Loading MusicGen model (size: {model_size})...")
        
        # Model name mapping
        model_names = {
            'small': 'facebook/musicgen-small',
            'medium': 'facebook/musicgen-medium',
            'large': 'facebook/musicgen-large',
            'melody': 'facebook/musicgen-melody'
        }
        
        model_name = model_names.get(model_size, 'facebook/musicgen-small')
        
        try:
            # Load model and processor
            _cached_model = MusicgenForConditionalGeneration.from_pretrained(model_name)
            _cached_processor = AutoProcessor.from_pretrained(model_name)
            
            # Determine device
            if device is None:
                device = "cuda:0" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
            
            # Move model to device
            _cached_model.to(device)
            logger.info(f"Model loaded successfully on {device}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    return _cached_model, _cached_processor, device

def generate_music_with_musicgen(prompt, duration=10, temperature=1.0, top_k=250, top_p=0.9, 
                                 guidance_scale=3.0, model_size='small'):
    """
    Generate music using Meta's MusicGen model.
    
    Args:
        prompt (str): Text description of the desired music
        duration (float): Duration of the generated music in seconds
        temperature (float): Sampling temperature (higher = more random)
        top_k (int): Top-k sampling parameter
        top_p (float): Top-p (nucleus) sampling parameter
        guidance_scale (float): Classifier-free guidance scale
        model_size (str): Model size to use ('small', 'medium', 'large')
    
    Returns:
        dict: Contains 'filename', 'filepath', and generation metadata
    """
    
    try:
        # Load model and processor
        model, processor, device = load_musicgen_model(model_size)
        
        logger.info(f"Generating music with prompt: '{prompt}'")
        logger.info(f"Parameters: duration={duration}s, temperature={temperature}, guidance_scale={guidance_scale}")
        
        # Calculate max_new_tokens based on duration
        # MusicGen uses ~50 tokens per second of audio
        max_new_tokens = int(duration * 50)
        
        # Prepare inputs
        inputs = processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )
        
        # Move inputs to device
        if device != "cpu":
            inputs = inputs.to(device)
        
        # Generate audio
        with torch.no_grad():
            audio_values = model.generate(
                **inputs,
                do_sample=True,
                guidance_scale=guidance_scale,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p
            )
        
        # Get sampling rate
        sampling_rate = model.config.audio_encoder.sampling_rate
        
        # Convert to numpy and move to CPU
        audio_array = audio_values[0, 0].cpu().numpy()
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"generated_{timestamp}.wav"
        filepath = os.path.join('music', filename)
        
        # Ensure music directory exists
        os.makedirs('music', exist_ok=True)
        
        # Save audio file
        scipy.io.wavfile.write(filepath, rate=sampling_rate, data=audio_array)
        
        logger.info(f"Music generated successfully: {filename}")
        
        return {
            'filename': filename,
            'filepath': filepath,
            'sample_rate': sampling_rate,
            'duration': duration,
            'prompt': prompt,
            'model_size': model_size,
            'temperature': temperature,
            'guidance_scale': guidance_scale
        }
        
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise Exception(f"Music generation failed: {str(e)}")

def generate_with_audio_prompt(audio_array, sampling_rate, text_prompt=None, 
                               duration=10, guidance_scale=3.0, model_size='small'):
    """
    Generate music continuation based on an audio prompt.
    
    Args:
        audio_array (np.ndarray): Input audio array
        sampling_rate (int): Sampling rate of the input audio
        text_prompt (str): Optional text prompt to guide generation
        duration (float): Duration of additional music to generate
        guidance_scale (float): Classifier-free guidance scale
        model_size (str): Model size to use
    
    Returns:
        dict: Contains generated audio information
    """
    
    try:
        # Load model and processor
        model, processor, device = load_musicgen_model(model_size)
        
        logger.info("Generating music with audio prompt")
        
        # Calculate max_new_tokens
        max_new_tokens = int(duration * 50)
        
        # Prepare inputs
        if text_prompt:
            inputs = processor(
                audio=audio_array,
                sampling_rate=sampling_rate,
                text=[text_prompt],
                padding=True,
                return_tensors="pt",
            )
        else:
            inputs = processor(
                audio=audio_array,
                sampling_rate=sampling_rate,
                padding=True,
                return_tensors="pt",
            )
        
        # Move inputs to device
        if device != "cpu":
            inputs = inputs.to(device)
        
        # Generate audio
        with torch.no_grad():
            audio_values = model.generate(
                **inputs,
                do_sample=True,
                guidance_scale=guidance_scale,
                max_new_tokens=max_new_tokens
            )
        
        # Process output
        if hasattr(processor, 'batch_decode'):
            audio_values = processor.batch_decode(audio_values, padding_mask=inputs.padding_mask)
            audio_array = audio_values[0]
        else:
            audio_array = audio_values[0, 0].cpu().numpy()
        
        # Save audio file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"continued_{timestamp}.wav"
        filepath = os.path.join('music', filename)
        
        scipy.io.wavfile.write(filepath, rate=model.config.audio_encoder.sampling_rate, data=audio_array)
        
        return {
            'filename': filename,
            'filepath': filepath,
            'sample_rate': model.config.audio_encoder.sampling_rate,
            'duration': duration,
            'text_prompt': text_prompt,
            'type': 'audio_continuation'
        }
        
    except Exception as e:
        logger.error(f"Audio continuation failed: {str(e)}")
        raise

def get_available_models():
    """
    Return list of available MusicGen models.
    """
    return [
        {'name': 'musicgen-small', 'size': '300M', 'description': 'Fast generation, good quality'},
        {'name': 'musicgen-medium', 'size': '1.5GB', 'description': 'Balanced speed and quality'},
        {'name': 'musicgen-large', 'size': '3.3GB', 'description': 'Best quality, slower generation'},
        {'name': 'musicgen-melody', 'size': '1.5GB', 'description': 'Melody-conditioned generation'}
    ]

def test_musicgen():
    """
    Test function to verify MusicGen is working.
    """
    try:
        logger.info("Testing MusicGen installation...")
        
        # Test with a simple prompt
        result = generate_music_with_musicgen(
            prompt="A peaceful piano melody",
            duration=5,
            model_size='small'
        )
        
        logger.info(f"Test successful! Generated: {result['filename']}")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Run test when module is executed directly
    test_musicgen()