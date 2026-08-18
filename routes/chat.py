from flask import Blueprint, request, jsonify

from services.chat.pipeline import ChatPipeline

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("question", "").strip()

    if question == "":

        return jsonify({
            "success": False,
            "message": "Question cannot be empty."
        }), 400

    pipeline = ChatPipeline()

    response = pipeline.execute(question)

    return jsonify(response)