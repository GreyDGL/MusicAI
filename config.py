"""
Configuration file for MusicGen and application settings
"""

import os

# Application Settings
APP_CONFIG = {
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production'),
    'DATABASE_URI': 'sqlite:///database.db',
    'UPLOAD_FOLDER': 'music',
    'MAX_CONTENT_LENGTH': 100 * 1024 * 1024,  # 100MB max file size
    'PORT': 8080,
    'DEBUG': True
}

# MusicGen Model Settings
MUSICGEN_CONFIG = {
    # Default model to use ('small', 'medium', 'large', 'melody')
    'DEFAULT_MODEL': 'small',
    
    # Model cache directory (where models are downloaded)
    'CACHE_DIR': os.path.expanduser('~/.cache/huggingface/hub'),
    
    # Device selection ('cuda', 'mps', 'cpu', or None for auto-detect)
    'DEVICE': None,  # Will auto-detect: CUDA > MPS > CPU
    
    # Generation defaults
    'DEFAULT_DURATION': 10,  # seconds
    'DEFAULT_TEMPERATURE': 1.0,
    'DEFAULT_GUIDANCE_SCALE': 3.0,
    'DEFAULT_TOP_K': 250,
    'DEFAULT_TOP_P': 0.9,
    
    # Maximum generation limits
    'MAX_DURATION': 30,  # Maximum duration in seconds
    
    # Model descriptions
    'MODELS': {
        'small': {
            'name': 'facebook/musicgen-small',
            'size': '300M',
            'description': 'Fast generation with good quality. Best for quick prototyping.',
            'recommended_for': 'Quick tests and iterations'
        },
        'medium': {
            'name': 'facebook/musicgen-medium',
            'size': '1.5GB',
            'description': 'Balanced speed and quality. Good for most use cases.',
            'recommended_for': 'General music generation'
        },
        'large': {
            'name': 'facebook/musicgen-large',
            'size': '3.3GB',
            'description': 'Best quality but slower. Use for final productions.',
            'recommended_for': 'High-quality final outputs'
        },
        'melody': {
            'name': 'facebook/musicgen-melody',
            'size': '1.5GB',
            'description': 'Specialized for melody generation with audio conditioning.',
            'recommended_for': 'Melody-focused compositions'
        }
    }
}

# Audio Processing Settings
AUDIO_CONFIG = {
    'SUPPORTED_FORMATS': ['.wav', '.mp3', '.flac', '.m4a'],
    'DEFAULT_SAMPLE_RATE': 32000,
    'WAVEFORM_SAMPLES': 1024
}

# Evaluation Settings
EVALUATION_CONFIG = {
    'CRITERIA': [
        {
            'id': 'melodic_content',
            'name': 'Melodic Content',
            'description': 'Clarity, development, and thematic material',
            'weight': 0.2
        },
        {
            'id': 'instrumentation',
            'name': 'Instrumentation/Timbre',
            'description': 'Authenticity, clarity, and timbral accuracy',
            'weight': 0.2
        },
        {
            'id': 'rhythmic_structure',
            'name': 'Rhythmic Structure',
            'description': 'Groove, timing, and forward motion',
            'weight': 0.2
        },
        {
            'id': 'mood_alignment',
            'name': 'Mood/Emotional Alignment',
            'description': 'Matches prompt and emotional impact',
            'weight': 0.2
        },
        {
            'id': 'audio_quality',
            'name': 'Audio Quality',
            'description': 'Technical quality, artifacts, and balance',
            'weight': 0.2
        }
    ]
}

# Prompt Templates and Examples
PROMPT_TEMPLATES = {
    'classical': [
        "A {mood} {instrument} sonata in the style of {composer}",
        "Baroque {instrument} piece with complex counterpoint",
        "{mood} classical symphony with {instruments}"
    ],
    'electronic': [
        "{bpm} BPM {genre} track with {elements}",
        "Ambient {mood} soundscape with {textures}",
        "Electronic dance music with {bass_type} bass and {synth_type}"
    ],
    'world': [
        "{culture} traditional music with {instruments}",
        "{region} folk melody featuring {instrument}",
        "World fusion combining {culture1} and {culture2} styles"
    ],
    'jazz': [
        "{tempo} jazz {instrument} solo with {accompaniment}",
        "{era} jazz standard with {mood} feel",
        "Smooth jazz with {instrument} lead and {backing}"
    ]
}

# Logging Configuration
LOGGING_CONFIG = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'FILE': 'musicgen.log'
}