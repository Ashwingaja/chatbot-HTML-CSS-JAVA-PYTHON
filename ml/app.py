from flask import Flask, render_template, request, jsonify
from chat import get_response
import mysql.connector

app = Flask(__name__, template_folder="templates", static_folder="static")

# Function to establish database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",  # e.g., "localhost"
        user="root",
        password="ashwin",
        database="chatbot_db"
    )

# Function to store chat interactions
def store_chat(user_input, bot_response):
    try:
        db = connect_db()
        cursor = db.cursor()
        sql = "INSERT INTO chat_history (user_input, bot_response) VALUES (%s, %s)"
        values = (user_input, bot_response)
        cursor.execute(sql, values)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error storing chat: {e}")

@app.get("/")
def index_get():
    return render_template("base.html")
    
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    if not text:
        return jsonify({"answer": "Invalid input!"})

    response = get_response(text)

    # Store the chat in MySQL
    store_chat(text, response)

    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)
