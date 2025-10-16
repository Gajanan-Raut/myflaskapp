# from flask import Flask, render_template, request, session
# from openai import OpenAI

# app = Flask(__name__)
# app.secret_key = "your_secret_key_here"  # needed for sessions
# client = OpenAI(api_key="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")

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if "chat_history" not in session:
#         session["chat_history"] = []

#     if request.method == "POST":
#         user_message = request.form["message"]

#         # Add user message to chat history
#         session["chat_history"].append({"role": "user", "content": user_message})

#         # Send full history to GPT
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=session["chat_history"]
#         )

#         gpt_reply = response.choices[0].message.content

#         # Add GPT reply to chat history
#         session["chat_history"].append({"role": "assistant", "content": gpt_reply})
#         session.modified = True  # tell Flask we changed the session

#     return render_template("index.html", chat_history=session["chat_history"])

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, session
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_message = request.form["message"]
        session["chat_history"].append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=session["chat_history"]
        )

        gpt_reply = response.choices[0].message.content
        session["chat_history"].append({"role": "assistant", "content": gpt_reply})
        session.modified = True

    return render_template("index.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
