

import google.generativeai as genai
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


genai.configure(api_key="AIzaSyCK8C-NzbiisJp3COPdtaENthBIQhL5TOc")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings
                              )

convo = model.start_chat(history=[
])
    

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    # User request to model
    user_message = request.form.get("user_message")
    print(f"Received user message: {user_message}")  

    if not user_message:
        return jsonify({"error": "Missing user message"}), 400

    try:
        # model responce
        convo.send_message(user_message)
        response = convo.last.text
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error sending message to Gemini: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)

