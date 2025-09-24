from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MusicFile(db.Model):
    __tablename__ = 'music_files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    file_hash = db.Column(db.String(32), unique=True, nullable=False)
    prompt = db.Column(db.Text)
    generation_params = db.Column(db.Text)  # JSON string of generation parameters
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    evaluations = db.relationship('Evaluation', backref='music_file', lazy=True, cascade='all, delete-orphan')
    
    def is_evaluated(self):
        """Check if this music file has any evaluations."""
        return len(self.evaluations) > 0
    
    def get_average_rating(self):
        """Calculate average overall rating from all evaluations."""
        if not self.evaluations:
            return None
        ratings = [e.overall_rating for e in self.evaluations if e.overall_rating]
        return sum(ratings) / len(ratings) if ratings else None

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music_files.id'), nullable=False)
    
    # Evaluation criteria (1-5 scale)
    melodic_content = db.Column(db.Integer)
    melodic_notes = db.Column(db.Text)
    
    instrumentation = db.Column(db.Integer)
    instrumentation_notes = db.Column(db.Text)
    
    rhythmic_structure = db.Column(db.Integer)
    rhythmic_notes = db.Column(db.Text)
    
    mood_alignment = db.Column(db.Integer)
    mood_notes = db.Column(db.Text)
    
    audio_quality = db.Column(db.Integer)
    audio_notes = db.Column(db.Text)
    
    overall_rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    
    evaluator_name = db.Column(db.String(100), default='Anonymous')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert evaluation to dictionary."""
        return {
            'id': self.id,
            'music_id': self.music_id,
            'melodic_content': self.melodic_content,
            'melodic_notes': self.melodic_notes,
            'instrumentation': self.instrumentation,
            'instrumentation_notes': self.instrumentation_notes,
            'rhythmic_structure': self.rhythmic_structure,
            'rhythmic_notes': self.rhythmic_notes,
            'mood_alignment': self.mood_alignment,
            'mood_notes': self.mood_notes,
            'audio_quality': self.audio_quality,
            'audio_notes': self.audio_notes,
            'overall_rating': self.overall_rating,
            'comments': self.comments,
            'evaluator_name': self.evaluator_name,
            'created_at': self.created_at.isoformat()
        }