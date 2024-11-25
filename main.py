from flask import Flask, render_template, request, jsonify
from chatbot import Chat, register_call
import os
import random
import re
import pandas as pd

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
# chat_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example.template")
# chat = Chat(chat_template)

@app.route("/")
def home():
    
    return render_template("index.html")

tatics = {"TA0043":"Reconnaissance"}

def queryFilter(query):
    if query[0] == "T" and (len(query)>4 and len(query)<10):
        searchCata = "technique ID"
        return searchCata
    elif query[0:3] == "APT" and query[3] == '-':
        searchCata = "group name"
        return searchCata
    elif query[0] == "G" and len(query) < 6:
        searchCata = "group ID"
        return searchCata
    else:
        return
        

# Extract query from user message
def extract_query(user_message):
    patterns = [
        r"what is (?P<query>.+)",
        r"who is (?P<query>.+)",
        r"tell me about (?P<query>.+)",
        r"do you know about (?P<query>.+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, user_message, re.IGNORECASE)
        if match:
            return match.group("query").strip()
    # If no pattern matches, return the original message
    return user_message.strip()

data_csv = "updated_aptgroup_relationships.csv"


# Generic response generator
def generate_generic_response(query, searchCata):
    try:
        # Load the CSV file
        data = pd.read_csv(data_csv)

        # Define the columns to search for the query
        search_columns = ["group ID", "group name", "technique ID", "technique name", 
                          "group mapping description", "technique description", 
                          "technique tactics", "technique platforms", 
                          "is sub-technique of target", "target sub-technique of", 
                          "technique supports remote"]
        
        if searchCata != None:
            print(searchCata)
            search_columns = search_columns
    
        match = data[
            data[search_columns].apply(
                lambda row: any(row.astype(str).str.contains(query, case=False, na=False)), axis=1
            )
        ]    

        # Filter rows where the query matches any of the search columns (case-insensitive)
        # match = data[
        #     data[search_columns].apply(
        #         lambda row: any(row.astype(str).str.contains(query, case=False, na=False)), axis=1
        #     )
        # ]

        # If a match is found, format the response
        if not match.empty:
            result = match.iloc[0]  # Get the first match
            if searchCata == "technique ID":
                response = (

                f"**Technique Details**<br>"
                f"----------------------<br>"
                f"Technique ID: {result['technique ID']}<br>"
                f"Technique Name: {result['technique name']}<br>"
                f"Technique Description:<br>{result['technique description']}<br><br>"

                f"**APT Group Information**<br>"
                f"-------------------------<br>"
                f"Group ID: {result['group ID']}<br>"
                f"Group Name: {result['group name']}<br><br>"

                f"**Additional Information**<br>"
                f"---------------------------<br>" 
                f"Group Mapping Description: {result['group mapping description']}<br>"
                f"Technique Tactics: {result['technique tactics']}<br>"
                f"Technique Platforms: {result['technique platforms']}<br>"
                f"Is Sub-Technique of Target: {result['is sub-technique of target']}<br>"
                f"Target Sub-Technique Of: {result['target sub-technique of']}<br>"
                f"Technique Supports Remote: {result['technique supports remote']}<br>"
                )

                return response
            elif searchCata == "group name" | search_columns == "group ID":
                response = (

                f"**APT Group Information**<br>"
                f"-------------------------<br>"
                f"Group ID: {result['group ID']}<br>"
                f"Group Name: {result['group name']}<br><br>"

                f"---------------------------<br>" 
                f"Group Mapping Description: {result['group mapping description']}<br>"
                f"Technique Tactics: {result['technique tactics']}<br>"
                f"Technique Platforms: {result['technique platforms']}<br>"
                f"Is Sub-Technique of Target: {result['is sub-technique of target']}<br>"
                f"Target Sub-Technique Of: {result['target sub-technique of']}<br>"
                f"Technique Supports Remote: {result['technique supports remote']}<br>"
                )

                return response
            elif searchCata == "group name":
                return


        # If no match is found, return a generic message
        return f"Sorry, I couldn't find information about '{query}'."

    except Exception as e:
        return f"An error occurred while processing your query: {str(e)}"
    ### generic old code from here
    # responses = [
    #     f"I'm not sure about '{query}', but it sounds interesting!",
    #     f"That's a great question about '{query}'. I'll need to think about it!",
    #     f"I don't have enough information on '{query}', but I'd love to learn more.",
    #     f"Hmm, I'm not sure about '{query}'. Could you tell me more?",
    #     f"'{query}' is a fascinating topic. I'll try to find out more for next time!",
    # ]
    # return random.choice(responses)

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    user_message = request.json.get('message', "").strip()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Extract the query from the user's message
        query = extract_query(user_message)

        searchCata = queryFilter(query)
        
        # Get the chatbot's response
        bot_response = generate_generic_response(query, searchCata)

        # If no response is found, return a random fallback response
        if not bot_response:
            bot_response = random.choice(fallback_responses)

        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
  app.run(debug=True)