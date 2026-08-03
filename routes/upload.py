from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path

from services.knowledge_base import KnowledgeBase

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = Path("uploads")


@upload_bp.route("/upload", methods=["POST","GET"])
def upload_files():

    if "files" not in request.files:
        return jsonify({
            "success": False,
            "message": "No files uploaded."
        }), 400

    files = request.files.getlist("files")

    if len(files) == 0:
        return jsonify({
            "success": False,
            "message": "Please select at least one PDF."
        }), 400

    # Create uploads folder if it doesn't exist
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    # Clear old PDFs
    for pdf in UPLOAD_FOLDER.glob("*.pdf"):
        pdf.unlink()

    # Save uploaded PDFs
    for file in files:

        if file.filename == "":
            continue

        filename = secure_filename(file.filename)

        file.save(
            UPLOAD_FOLDER / filename
        )

    # Build Knowledge Base
    knowledge_base = KnowledgeBase()

    result = knowledge_base.build("uploads")

    return jsonify({
        "success": True,
        "message": "Knowledge Base created successfully.",
        "documents": result["documents"],
        "chunks": result["chunks"]
    })