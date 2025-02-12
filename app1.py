import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Use PostgreSQL database from Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define JournalEntry model
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(100), default=datetime.utcnow)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Save a new journal entry
@app.route('/save_entry', methods=['POST'])
def save_entry():
    data = request.json
    new_entry = JournalEntry(text=data['text'], date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Entry saved!"}), 201

# Get all journal entries
@app.route('/get_entries', methods=['GET'])
def get_entries():
    entries = JournalEntry.query.order_by(JournalEntry.id.desc()).all()
    return jsonify([{"text": entry.text, "date": entry.date} for entry in entries])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
