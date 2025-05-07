from flask import Blueprint, request, jsonify
from backend.models.schemas import ChatResponse,ChatRequest
from backend.services.generator_service import chat_medical_text
from pydantic import ValidationError

chat_bp  = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        req = ChatRequest(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session_id,answer,history = chat_medical_text(req.question, req.profil,session_id=req.session_id)

    resp=ChatResponse(
        session_id=session_id,
        answer=answer,
        history=history
        
    )
    return jsonify(resp.dict())
