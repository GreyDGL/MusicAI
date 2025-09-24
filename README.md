# Music AI Evaluation System

A comprehensive web-based system for evaluating AI-generated music with structured criteria based on expert feedback.

## Features

### 1. Music Generation Interface
- Text prompt input for music generation
- Adjustable parameters (duration, temperature, model size)
- MusicGen API integration placeholder (ready for actual implementation)
- Example prompts for various music styles

### 2. Music Evaluation System
- Structured evaluation criteria:
  - Melodic Content (clarity, development, thematic material)
  - Instrumentation/Timbre Accuracy (authenticity, clarity, synthetic elements)
  - Rhythmic Structure (groove, timing, forward motion)
  - Mood/Emotional Alignment (matches prompt, emotional impact)
  - Audio Quality (artifacts, balance, clarity)
  - Overall Rating
- Visual audio waveform display
- Star rating system (1-5 scale) for each criterion
- Free-form comments for detailed feedback
- Support for multiple evaluations per music file

### 3. Dashboard
- Overview statistics (total files, evaluations, pending reviews, average rating)
- Recent music files display
- Top-rated music leaderboard
- Rating distribution visualization
- Quick action buttons

### 4. Music Library Management
- Automatic folder scanning for new music files
- Support for WAV, MP3, FLAC, M4A formats
- File deduplication using MD5 hashing
- Metadata tracking (prompt, generation parameters, timestamps)

### 5. Data Export
- Export all evaluations as JSON
- Comprehensive data structure with all metrics and comments
- Ready for analysis and reporting

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the application at: http://localhost:8080

## Usage

### Quick Start
1. Click "Scan Folder" to import existing music files from the `music/` directory
2. Go to "Evaluate" to listen to and evaluate music
3. Use "Generate" to create new music (currently uses placeholder)
4. View statistics and trends on the Dashboard
5. Export evaluation data using the Export button

### Evaluation Process
1. Select a music file from the library
2. Listen to the audio with visual waveform
3. Rate each criterion on a 1-5 scale
4. Add detailed notes for each criterion
5. Provide overall comments
6. Submit evaluation

### Music Generation (Placeholder)
The system includes a placeholder for MusicGen integration. To connect actual MusicGen:
1. Install the audiocraft library
2. Update `musicgen_api.py` with actual MusicGen model calls
3. The interface is already prepared for real generation

## File Structure
```
musicAI/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── musicgen_api.py       # MusicGen integration (placeholder)
├── requirements.txt      # Python dependencies
├── music/                # Music files storage
├── static/
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── main.js      # Frontend JavaScript
├── templates/
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard
│   ├── generate.html    # Music generation
│   └── evaluate.html    # Evaluation interface
└── database.db          # SQLite database
```

## API Endpoints

- `GET /` - Dashboard
- `GET /generate` - Generation interface
- `GET /evaluate` - Evaluation interface
- `GET /api/music/list` - List all music files
- `GET /api/music/scan` - Scan folder for new music
- `GET /api/music/<id>/stream` - Stream music file
- `POST /api/generate` - Generate new music (placeholder)
- `POST /api/evaluate` - Submit evaluation
- `GET /api/evaluations/<music_id>` - Get evaluations for a music file
- `GET /api/export/evaluations` - Export all evaluation data

## Database Schema

### MusicFile Table
- id (Primary Key)
- filename
- filepath
- file_hash (MD5, unique)
- prompt
- generation_params (JSON)
- created_at

### Evaluation Table
- id (Primary Key)
- music_id (Foreign Key)
- melodic_content (1-5)
- melodic_notes (text)
- instrumentation (1-5)
- instrumentation_notes (text)
- rhythmic_structure (1-5)
- rhythmic_notes (text)
- mood_alignment (1-5)
- mood_notes (text)
- audio_quality (1-5)
- audio_notes (text)
- overall_rating (1-5)
- comments (text)
- evaluator_name
- created_at

## Technologies Used
- Backend: Flask, SQLAlchemy, Flask-Migrate
- Frontend: Bootstrap 5, WaveSurfer.js, Chart.js
- Database: SQLite
- Audio Processing: librosa (ready for analysis features)

## Future Enhancements
- Real MusicGen integration
- Batch evaluation mode
- User authentication
- Advanced audio analysis features
- CSV export option
- Comparison view for multiple evaluations
- Automated quality metrics