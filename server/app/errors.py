from werkzeug.exceptions import HTTPException
from flask import jsonify
import traceback

def handle_exception(e):
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({"error": str(e)}).data
        response.content_type = "application/json"
        return response
    
    traceback.print_exc()

    return jsonify({
        "error": "Internal server error.",
        "message": str(e)
    }), 500