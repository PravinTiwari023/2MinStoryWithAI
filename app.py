import re
from flask import Flask, render_template, request, jsonify
from database import save_vote_to_db, load_mystery_from_db, init_db, collect_vote_counts
from sqlalchemy.exc import IntegrityError  # Import IntegrityError for exception handling
from Gemini import generate_text

app = Flask(__name__)

@app.route('/')
def index():
    mystery = load_mystery_from_db()
    vote_counts = collect_vote_counts()
    return render_template('index.html', mystery=mystery, vote_counts=vote_counts)

@app.route('/submit', methods=['POST'])
def submit():
    user_thought = request.form['thought']
    ai_message = generate_text(user_thought)  # Placeholder for AI response generation
    return jsonify({'ai_message': ai_message})

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

# Function to validate email format
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def generate_ai_response(thought):
    # Placeholder for actual AI logic
    return "This is a generated response to: " + thought

if __name__ == '__main__':
    app.run(debug=True)
