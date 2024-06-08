from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_thought = request.form['thought']
    ai_message = "AI Response: " + generate_ai_response(user_thought)  # Placeholder for AI response generation
    return jsonify({'ai_message': ai_message})

def generate_ai_response(thought):
    # Placeholder for actual AI logic
    return "This is a generated response to: " + thought

if __name__ == '__main__':
    app.run(debug=True)