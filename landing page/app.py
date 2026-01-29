from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funnel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELS (Keep these consistent) ---
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- THE ROUTES (This connects the pages) ---

# 1. LANDING PAGE
@app.route('/')
def home():
    return render_template('index.html')

# 2. OPT-IN LOGIC (Connects Page 1 to Page 2)
@app.route('/optin', methods=['POST'])
def optin():
    email = request.form.get('email')
    
    if email:
        # Save to DB (Simple check to avoid duplicates)
        existing = Lead.query.filter_by(email=email).first()
        if not existing:
            new_lead = Lead(email=email)
            db.session.add(new_lead)
            db.session.commit()
    
    # CRITICAL: This redirects the user to the Training Video page
    return redirect(url_for('training'))

# 3. TRAINING PAGE
@app.route('/training-video')
def training():
    return render_template('training.html')

# 4. APPLICATION PAGE (Connects Page 2 to Page 3)
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        # (Here you would save the application answers)
        return "<h1>Application Submitted! We will contact you shortly.</h1>"
    
    return render_template('apply.html')

# --- RUN APP ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)