from flask import Flask, request, redirect, url_for, render_template, flash
import secrets

app = Flask(__name__)

# Generate a random secret key
app.secret_key = secrets.token_hex(16)  # Generates a random secret key

events = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Here, you could validate and store the credentials in memory if needed.
        flash("User registered successfully!")
        return redirect(url_for('calendar'))

    return render_template('sign_up_page.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', events=events)

@app.route('/handle_login', methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate user credentials here (in-memory or simple checks)
        flash("Login successful!")
        return redirect(url_for('calendar'))

    flash("Invalid email or password")
    return redirect(url_for('home'))

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        date = request.form['date']
        email = request.form['email']

        # Create a new event
        new_event = {
            "title": title,
            "start": date,
            "description": description,
            "user_email": email
        }

        events.append(new_event)

        flash("Event added successfully!")
        return redirect(url_for('calendar'))
    return render_template('add_event.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
