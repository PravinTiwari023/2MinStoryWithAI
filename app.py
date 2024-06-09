from flask import Flask, render_template, request, jsonify
from database import load_mystery_from_db

app = Flask(__name__)

@app.route('/')
def index():
    mystery = load_mystery_from_db()
    return render_template('index.html', mystery=mystery)

@app.route('/submit', methods=['POST'])
def submit():
    user_thought = request.form['thought']
    ai_message = "AI Response: " + generate_ai_response(user_thought)  # Placeholder for AI response generation
    return jsonify({'ai_message': ai_message})

@app.route('/vote', methods=['POST'])
def vote():
    vote_value = request.form['vote']
    email = request.form['email']
    # Here you would handle the vote, e.g., save it to the database
    print(f"Vote received: {vote_value} by {email}")
    return jsonify({'message': 'Vote received'})

def generate_ai_response(thought):
    # Placeholder for actual AI logic
    return "This is a generated response to: " + thought

if __name__ == '__main__':
    app.run(debug=True)
