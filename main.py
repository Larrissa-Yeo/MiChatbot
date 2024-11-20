from flask import Flask, render_template, request, jsonify
from chatbot import Chat, register_call
import os
import random

#app.py
#import files
app = Flask(__name__)

# Fallback responses
fallback_responses = [
    "I'm not sure how to answer that, but let's keep chatting!",
    "That's an interesting question. I'll need to think about it more.",
    "Hmm, I don't know about that. Can you ask something else?",
]

## Using a sample response template
chat_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example.template")
chat = Chat(chat_template)

@app.route("/")
def home():
    
    return render_template("index.html")

# Generic response generator
def generate_generic_response(query):
    responses = [
        f"I'm not sure about '{query}', but it sounds interesting!",
        f"That's a great question about '{query}'. I'll need to think about it!",
        f"I don't have enough information on '{query}', but I'd love to learn more.",
        f"Hmm, I'm not sure about '{query}'. Could you tell me more?",
        f"'{query}' is a fascinating topic. I'll try to find out more for next time!",
    ]
    return random.choice(responses)

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    user_message = request.json.get('message', "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Get the chatbot's response
        bot_response = generate_generic_response(user_message)

        # If no response is found, return a random fallback response
        if not bot_response:
            bot_response = random.choice(fallback_responses)

        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
  app.run(debug=True)