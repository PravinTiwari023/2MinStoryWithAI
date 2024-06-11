from flask import Flask, render_template, request, jsonify
from database import save_feedback_to_db, load_mystery_from_db, init_db, collect_vote_counts, save_vote_to_db
from sqlalchemy.exc import IntegrityError  # Import IntegrityError for exception handling
from Gemini import generate_text
import re

app = Flask(__name__)

# Home route to render the main page
@app.route('/')
def index():
    mystery = load_mystery_from_db()
    vote_counts = collect_vote_counts()
    return render_template('index.html', mystery=mystery, vote_counts=vote_counts)

# Route to handle user thought submission
@app.route('/submit', methods=['POST'])
def submit():
    user_thought = request.form['thought']
    ai_message = generate_text(user_thought)  # Placeholder for AI response generation
    return jsonify({'ai_message': ai_message})

# Route to handle voting
@app.route('/vote', methods=['POST'])
def vote():
    vote_value = request.form['vote']
    email = request.form['email']

    print(f"Received vote: {vote_value}, email: {email}")

    # Validate email format
    if not validate_email(email):
        print("Invalid email format")
        return jsonify({'message': 'Invalid email address'}), 400

    # Save the vote to the database
    try:
        save_vote_to_db(vote_value, email)
        return jsonify({'message': 'Vote received'})
    except IntegrityError:
        print("Email already voted")
        return jsonify({'message': 'Email already voted. Please use a different email.'}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'An error occurred'}), 500

# Route to handle feedback submission
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    feedback = data.get('feedback')

    # Validate email format
    if not validate_email(email):
        return jsonify({'message': 'Invalid email address', 'success': False}), 400

    # Save feedback to the database
    try:
        save_feedback_to_db(name, email, feedback)
        return jsonify({'message': 'Thank you for your valuable feedback.', 'success': True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'An error occurred', 'success': False}), 500

# Function to validate email format using regex
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Entry point of the application
if __name__ == '__main__':
    app.run(debug=True)
