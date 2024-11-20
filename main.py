from flask import Flask, render_template, request, jsonify

#app.py
#import files
app = Flask(__name__)
@app.route("/")
def home():
  return "Hello, This is Flask Application"
if __name__ == "__main__":
  app.run()