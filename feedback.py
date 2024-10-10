import openai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import os
from dotenv import load_dotenv

load_dotenv()


# Set your OpenAI API key directly (for testing only)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
CORS(app)  # Enable CORS for all routes

def get_feedback_response(message):
    """
    This function uses the latest Chat Completion API method to generate a structured response
    specifically for collecting event feedback using the gpt-4 model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the correct model identifier
            messages=[
                {"role": "system", "content": "You are a helpful assistant collecting feedback for an event at People+AI. Questions to ask but ask one by one - Do you have any specific feedback for either Project Sukoon or Sunva?, - Was the SoulUp (Partner Feature) valuable for you?, - Do you have any suggestions for Partners we should feature in future mental health or health events?, aat last mention - Thank you for coming! Do follow us on Social Media (peopleplusai) and also check out the Use Case Garden that we spoke about (https://pplus.ai/usecasegarden)"},
                {"role": "user", "content": message}
            ],
            max_tokens=100,  # Optional: Adjust based on expected response length
            temperature=0.7  # Optional: Adjust creativity level
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    """
    Serve the HTML form for collecting feedback.
    """
    return render_template('index.html')

@app.route('/feedback', methods=['POST'])
def collect_feedback():
    """
    Flask endpoint to receive event feedback and return OpenAI-generated response using gpt-4.
    """
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call the function to get feedback response
    feedback_response = get_feedback_response(user_message)

    return jsonify({"feedback_response": feedback_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
