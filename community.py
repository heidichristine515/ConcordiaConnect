from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
migrate=Migrate(app, db)

# User model to define the structure of user data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords here

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    user_email = db.Column(db.String(120), nullable=False)  # User's email who created the event


# Create the database tables
with app.app_context():
    db.create_all()  # This creates the database file and tables


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please try another email.")
            return redirect(url_for('sign_up'))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("User registered successfully!")
        return redirect(url_for('calendar'))

    return render_template('sign_up_page.html')

@app.route('/calendar')
def calendar():
    events = Event.query.all()  # Get all events from the database
    return render_template('calendar.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')  # Optional
        date = request.form['date']
        user_email = request.form['email']  # Capture user email who added the event

            # Convert date from string to Python DateTime
        event_date = datetime.strptime(date, '%Y-%m-%d')

            # Create a new event and save it to the database
        new_event = Event(title=title, description=description, date=event_date, user_email=user_email)
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('calendar'))
    return render_template('add_event.html')


@app.route('/handle_login', methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        return redirect(url_for('calendar'))
    else:
        flash("Invalid email or password")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)