MusicAI - AI Music Generation & Evaluation System
==================================================

A comprehensive web-based system for generating and evaluating AI-generated music using Meta's MusicGen model with structured evaluation criteria.

REPOSITORY
----------
https://github.com/GreyDGL/MusicAI

OVERVIEW
--------
MusicAI combines state-of-the-art music generation with professional evaluation tools, enabling collaborative research and assessment of AI-generated music quality.

FEATURES
--------

Music Generation:
- Real MusicGen Integration: Uses Meta's MusicGen model for high-quality music generation
- Multiple Model Sizes: Small (300MB), Medium (1.5GB), Large (3.3GB), and Melody variants
- Customizable Parameters: Duration (1-30s), Temperature, Guidance Scale
- Text-to-Music: Generate music from natural language descriptions
- CLI Support: Generate music via command line or web interface

Music Evaluation System:
- Structured Criteria: Professional evaluation framework with 6 key aspects:
  * Melodic Content (clarity, development, thematic material)
  * Instrumentation/Timbre (authenticity, clarity, synthetic elements)
  * Rhythmic Structure (groove, timing, forward motion)
  * Mood/Emotional Alignment (prompt matching, emotional impact)
  * Audio Quality (artifacts, balance, clarity)
  * Overall Rating
- Visual Waveform Display: Interactive audio visualization with WaveSurfer.js
- Star Rating System: 1-5 scale for quantitative assessment
- Detailed Comments: Free-form feedback for qualitative insights

Collaboration & Sync:
- Git-Based Syncing: Share evaluations through GitHub
- Database Synchronization: All evaluations stored in SQLite database
- Multi-User Support: Multiple evaluators can work on the same dataset
- Export Functionality: Export all data as JSON for analysis

Dashboard & Analytics:
- Overview Statistics: Total files, evaluations, average ratings
- Rating Distribution: Visual charts showing rating patterns
- Top-Rated Music: Leaderboard of best-performing generations
- Recent Activity: Track latest evaluations and generations

PREREQUISITES
-------------
- Python 3.8 or higher
- Git
- 4GB+ RAM (8GB+ recommended for Medium/Large models)
- macOS, Linux, or Windows
- ~10GB free disk space (for model downloads)

INSTALLATION
------------

Automated Installation (Recommended):
1. Clone the repository:
   git clone https://github.com/GreyDGL/MusicAI.git
   cd MusicAI

2. Run installation script:
   ./install.sh  (macOS/Linux)
   OR
   python install.py  (Windows)

3. Start the application:
   python app.py

Manual Installation:
1. Clone repository:
   git clone https://github.com/GreyDGL/MusicAI.git
   cd MusicAI

2. Create virtual environment:
   python -m venv venv
   source venv/bin/activate  (macOS/Linux)
   OR
   venv\Scripts\activate  (Windows)

3. Install dependencies:
   pip install -r requirements.txt
   pip install -r requirements_musicgen.txt

4. Start application:
   python app.py

USAGE
-----

Web Interface:
1. Start the application: python app.py
2. Open browser: http://localhost:8080
3. Navigate through tabs:
   - Generate: Create new music from text prompts
   - Evaluate: Listen and evaluate music files
   - Dashboard: View statistics and analytics
   - Export: Download evaluation data

Command Line Interface:
   # Generate music
   python musicgen_cli.py "A peaceful piano melody"

   # With options
   python musicgen_cli.py "Epic orchestral music" --duration 15 --model medium

   # List available models
   python musicgen_cli.py --list-models

Git Synchronization:
   # Get latest updates
   git pull origin main

   # Save your work
   git add .
   git commit -m "Added evaluations for jazz pieces"
   git push origin main

PROJECT STRUCTURE
-----------------
MusicAI/
├── app.py                    # Main Flask application
├── models.py                 # Database models (SQLAlchemy)
├── config.py                 # Configuration settings
├── musicgen_api.py          # MusicGen integration
├── musicgen_cli.py          # CLI for music generation
├── requirements.txt         # Python dependencies
├── requirements_musicgen.txt # MusicGen dependencies
├── install.sh               # Installation script
├── cleanup.sh               # Cleanup utility
├── run.sh                   # Launch script
├── music/                   # Generated music storage
├── instance/               # Instance-specific files
│   └── database.db        # SQLite database
├── static/                 # Frontend assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/              # HTML templates
    ├── base.html
    ├── index.html         # Dashboard
    ├── generate.html      # Generation interface
    └── evaluate.html      # Evaluation interface

CONFIGURATION
-------------

config.py Settings:
- PORT: Application port (default: 8080)
- MUSIC_FOLDER: Music storage location
- DATABASE_URL: Database connection
- MAX_DURATION: Maximum generation duration
- DEFAULT_MODEL: Default MusicGen model size

Model Performance:
+--------+-------+-----------+-----------------+---------+
| Model  | Size  | RAM Usage | Generation Time | Quality |
+--------+-------+-----------+-----------------+---------+
| Small  | 300MB | ~2GB      | 10-20s          | Good    |
| Medium | 1.5GB | ~6GB      | 20-40s          | Better  |
| Large  | 3.3GB | ~12GB     | 30-60s          | Best    |
+--------+-------+-----------+-----------------+---------+

EXAMPLE PROMPTS
---------------
- "Upbeat jazz piano with walking bass line"
- "Cinematic orchestral piece with strings and brass"
- "Lo-fi hip hop beat for studying"
- "Classical guitar with Spanish influences"
- "Ambient electronic with nature sounds"
- "90s rock anthem with power chords"
- "Smooth R&B with soul vocals feel"
- "Traditional Japanese music with koto and flute"

TROUBLESHOOTING
---------------

Common Issues:
- Port already in use: Change PORT in config.py
- Memory errors: Use smaller model or reduce duration
- Model download fails: Check internet connection and disk space
- Can't find Python: Use python3 instead of python
- Permission denied: Run with appropriate permissions or check file ownership

Reset & Cleanup:
   # Clean up and reset
   ./cleanup.sh

   # Remove models cache
   rm -rf ~/.cache/huggingface/hub/

COLLABORATION GUIDE
-------------------

For Project Owner:
1. Create GitHub repository
2. Push initial code
3. Add collaborators in Settings → Manage access
4. Share repository URL

For Collaborators:
1. Accept GitHub invitation
2. Clone repository
3. Make evaluations
4. Commit and push changes
5. Pull updates regularly

DEVELOPMENT
-----------

API Endpoints:
- GET / - Dashboard
- GET /generate - Generation page
- GET /evaluate - Evaluation page
- POST /api/generate - Generate music
- POST /api/evaluate - Submit evaluation
- GET /api/music/list - List music files
- GET /api/music/<id>/stream - Stream audio
- GET /api/export/evaluations - Export data

Database Schema:
- MusicFile: Stores generated music metadata
- Evaluation: Stores evaluation data and ratings

LICENSE
-------
This project uses open-source components including Meta's MusicGen model.

ACKNOWLEDGMENTS
---------------
- Meta AI for MusicGen model
- Flask community for web framework
- Bootstrap for UI components
- WaveSurfer.js for audio visualization

SUPPORT
-------
For issues or questions, please open an issue at: https://github.com/GreyDGL/MusicAI/issues