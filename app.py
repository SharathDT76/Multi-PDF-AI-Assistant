from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
from routes.upload import upload_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(upload_bp)
app.register_blueprint(chat_bp)

@app.route("/")
def home():
    return {
        "message": "Multi-PDF AI Assistant API is Running!"
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )