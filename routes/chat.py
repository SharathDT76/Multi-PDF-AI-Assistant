from flask import Blueprint, request,jsonify

from services.retriever import Retriever
from services.prompt_builder import PromptBuilder
from services.llm import LLMService

chat_bp = Blueprint("Chat" , __name__)

@chat_bp.route("/chat", methods = ["POST"])
def chat():
    data = request.get_json()

    question = data.get("question","").strip()

    if question =="":
        return jsonify({
            "success" : False,
            "message" : "Question cannot be empty"
        }) , 400

    retriever = Retriever()

    chunks = retriever.search(question)

    prompt_builder = PromptBuilder()

    prompt = prompt_builder.build_prompt(
        question,
        chunks
    )

    llm  = LLMService()
    answer = llm.generate_response(prompt)

    return jsonify({
        "success" : True,
        "question" : question,
        "answer" : answer,
        "sources" : chunks
    })
