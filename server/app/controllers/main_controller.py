from flask import request, jsonify
from . import main_api
from ..services.main_service import MainService
from ..k_means_handler.k_means_handler import vectorize_students, kmeans
from ..k_means_handler.vectorize_student import vectorize_student_by_id
from ..k_means_handler.distance import euclidean_distance_with_weights
import pandas as pd


@main_api.route("/", methods=["GET"])
def get_all_rooms_and_student_requests():
    main_service = MainService()
    rooms_data = main_service.get_all_rooms_data()
    student_requests_data = main_service.get_all_male_student_requests_data()
    return jsonify({
        "success": True,
        "message": "Successfully fetched all rooms and male student requests.",
        "rooms": rooms_data,
        "student_requests": student_requests_data
    }), 200
    
    
@main_api.route("/k-means-result", methods=["GET"])
def get_k_means_result():
    main_service = MainService()
    male_student_requests_data = main_service.get_all_male_student_requests_data()
    data_frame = pd.DataFrame(male_student_requests_data)
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    k=100
    result = kmeans(data_frame, k , weights, max_iter = 100)
    k_means_result = main_service.save_k_means_result(result)
    return jsonify({
        "success": True,
        "message": "Successfully fetched K-means result.",
        "id": k_means_result.id,
        "result": result
    }), 200
    
    
@main_api.route("/allocation-result", methods=["POST"])
def get_allocation_result():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid JSON data."
        }), 400
        
    k_means_result_id = data.get("id")
    if not k_means_result_id:
        return jsonify({
            "success": False,
            "message": "Missing required field: 'id'."
        }), 400
    
    main_service = MainService()
    k_means_result = main_service.get_k_means_result(k_means_result_id)
    if not k_means_result:
        return jsonify({
            "success": False,
            "message": "K-means result not found with the provided ID."
        }), 404
        
    # allocation_result = allocation_function(k_means_result)
    return jsonify({
        "success": True,
        "message": "Successfully fetched allocation result.",
        # "result": allocation_result
    }), 200