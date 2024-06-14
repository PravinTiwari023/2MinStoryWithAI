from flask import Flask, render_template, request, jsonify
from database import save_feedback_to_db, load_mystery_from_db, init_db, collect_vote_counts, save_vote_to_db
from sqlalchemy.exc import IntegrityError
from RagGemini import generate_content
from Gemini import generate_text
import re

# Initialize the Flask application
app = Flask(__name__)

# Home route to render the main page
@app.route('/')
def index():
    # Load the mystery content and vote counts from the database
    mystery_content = load_mystery_from_db()
    vote_counts = collect_vote_counts()
    return render_template('index.html', mystery=mystery_content, vote_counts=vote_counts)

# Route to handle user thought submission
@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve the user's thought from the form
    user_thought = request.form['thought']
    # Generate the AI response based on the user's thought
    ai_response = generate_text(user_thought)
    return jsonify({'ai_message': ai_response})

# Route to handle voting
@app.route('/vote', methods=['POST'])
def vote():
    # Retrieve the vote and email from the form
    vote_value = request.form['vote']
    email = request.form['email']

    print(f"Received vote: {vote_value}, email: {email}")

    # Validate the email format
    if not validate_email_format(email):
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
    # Retrieve feedback data from the JSON payload
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    feedback_text = data.get('feedback')

    # Validate the email format
    if not validate_email_format(email):
        return jsonify({'message': 'Invalid email address', 'success': False}), 400

    # Save the feedback to the database
    try:
        save_feedback_to_db(name, email, feedback_text)
        return jsonify({'message': 'Thank you for your valuable feedback.', 'success': True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'An error occurred', 'success': False}), 500

# Function to validate email format using regex
def validate_email_format(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Entry point of the application
if __name__ == '__main__':
    app.run(debug=True)
