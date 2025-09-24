from flask import Flask, render_template, request, jsonify, send_file
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import os
import json
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'music'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

from models import db, MusicFile, Evaluation

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_file_hash(filepath):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_page():
    return render_template('generate.html')

@app.route('/evaluate')
def evaluate_page():
    return render_template('evaluate.html')

@app.route('/api/music/list')
def list_music():
    """List all music files in the database."""
    music_files = MusicFile.query.order_by(MusicFile.created_at.desc()).all()
    return jsonify([{
        'id': m.id,
        'filename': m.filename,
        'prompt': m.prompt,
        'created_at': m.created_at.isoformat(),
        'evaluated': m.is_evaluated(),
        'average_rating': m.get_average_rating()
    } for m in music_files])

@app.route('/api/music/scan')
def scan_music_folder():
    """Scan music folder and add new files to database."""
    music_dir = app.config['UPLOAD_FOLDER']
    added_files = []
    
    for filename in os.listdir(music_dir):
        if filename.lower().endswith(('.wav', '.mp3', '.flac', '.m4a')):
            filepath = os.path.join(music_dir, filename)
            file_hash = get_file_hash(filepath)
            
            existing = MusicFile.query.filter_by(file_hash=file_hash).first()
            if not existing:
                music_file = MusicFile(
                    filename=filename,
                    filepath=filepath,
                    file_hash=file_hash,
                    prompt='Imported from folder'
                )
                db.session.add(music_file)
                added_files.append(filename)
    
    db.session.commit()
    return jsonify({
        'message': f'Added {len(added_files)} new files',
        'files': added_files
    })

@app.route('/api/music/<int:music_id>/stream')
def stream_music(music_id):
    """Stream a music file."""
    music_file = MusicFile.query.get_or_404(music_id)
    return send_file(music_file.filepath, mimetype='audio/wav')

@app.route('/api/generate', methods=['POST'])
def generate_music():
    """Generate music using MusicGen."""
    data = request.json
    prompt = data.get('prompt', '')
    duration = data.get('duration', 10)
    temperature = data.get('temperature', 1.0)
    model_size = data.get('model', 'small')
    guidance_scale = data.get('guidance_scale', 3.0)
    
    # Import MusicGen API
    from musicgen_api import generate_music_with_musicgen
    
    try:
        # Call actual MusicGen generation
        result = generate_music_with_musicgen(
            prompt=prompt,
            duration=duration,
            temperature=temperature,
            guidance_scale=guidance_scale,
            model_size=model_size
        )
        
        # Save generated file info to database
        music_file = MusicFile(
            filename=result['filename'],
            filepath=result['filepath'],
            file_hash=get_file_hash(result['filepath']),
            prompt=prompt,
            generation_params=json.dumps({
                'duration': duration,
                'temperature': temperature,
                'model_size': model_size,
                'guidance_scale': guidance_scale
            })
        )
        db.session.add(music_file)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'music_id': music_file.id,
            'message': 'Music generated successfully',
            'filename': result['filename']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Generation failed: {str(e)}'
        }), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate_music():
    """Submit an evaluation for a music file."""
    data = request.json
    music_id = data.get('music_id')
    
    music_file = MusicFile.query.get_or_404(music_id)
    
    evaluation = Evaluation(
        music_id=music_id,
        melodic_content=data.get('melodic_content'),
        melodic_notes=data.get('melodic_notes', ''),
        instrumentation=data.get('instrumentation'),
        instrumentation_notes=data.get('instrumentation_notes', ''),
        rhythmic_structure=data.get('rhythmic_structure'),
        rhythmic_notes=data.get('rhythmic_notes', ''),
        mood_alignment=data.get('mood_alignment'),
        mood_notes=data.get('mood_notes', ''),
        audio_quality=data.get('audio_quality'),
        audio_notes=data.get('audio_notes', ''),
        overall_rating=data.get('overall_rating'),
        comments=data.get('comments', ''),
        evaluator_name=data.get('evaluator_name', 'Anonymous')
    )
    
    db.session.add(evaluation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'evaluation_id': evaluation.id,
        'message': 'Evaluation submitted successfully'
    })

@app.route('/api/evaluations/<int:music_id>')
def get_evaluations(music_id):
    """Get all evaluations for a music file."""
    evaluations = Evaluation.query.filter_by(music_id=music_id).order_by(Evaluation.created_at.desc()).all()
    return jsonify([{
        'id': e.id,
        'melodic_content': e.melodic_content,
        'melodic_notes': e.melodic_notes,
        'instrumentation': e.instrumentation,
        'instrumentation_notes': e.instrumentation_notes,
        'rhythmic_structure': e.rhythmic_structure,
        'rhythmic_notes': e.rhythmic_notes,
        'mood_alignment': e.mood_alignment,
        'mood_notes': e.mood_notes,
        'audio_quality': e.audio_quality,
        'audio_notes': e.audio_notes,
        'overall_rating': e.overall_rating,
        'comments': e.comments,
        'evaluator_name': e.evaluator_name,
        'created_at': e.created_at.isoformat()
    } for e in evaluations])

@app.route('/api/export/evaluations')
def export_evaluations():
    """Export all evaluations as JSON."""
    evaluations = Evaluation.query.all()
    music_files = MusicFile.query.all()
    
    export_data = {
        'export_date': datetime.now().isoformat(),
        'music_files': [{
            'id': m.id,
            'filename': m.filename,
            'prompt': m.prompt,
            'generation_params': m.generation_params,
            'created_at': m.created_at.isoformat(),
            'evaluations': [{
                'melodic_content': e.melodic_content,
                'melodic_notes': e.melodic_notes,
                'instrumentation': e.instrumentation,
                'instrumentation_notes': e.instrumentation_notes,
                'rhythmic_structure': e.rhythmic_structure,
                'rhythmic_notes': e.rhythmic_notes,
                'mood_alignment': e.mood_alignment,
                'mood_notes': e.mood_notes,
                'audio_quality': e.audio_quality,
                'audio_notes': e.audio_notes,
                'overall_rating': e.overall_rating,
                'comments': e.comments,
                'evaluator_name': e.evaluator_name,
                'created_at': e.created_at.isoformat()
            } for e in m.evaluations]
        } for m in music_files]
    }
    
    return jsonify(export_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)