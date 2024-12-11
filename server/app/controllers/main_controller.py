from flask import request, jsonify
from . import main_api
from ..services.main_service import MainService
from ..k_means_handler.k_means_handler import kmeans
from ..Hung.weight import get_weight, re_calculate_weights
from ..Hung.solver import solver
from ..Hung.backtracking import greedy
from ..Hung.metric import mean_euclid_distance_of_room
import pandas as pd
import json

@main_api.route("/", methods=["GET"])
def get_all_rooms_and_student_requests():
    main_service = MainService()
    rooms_data = main_service.get_all_rooms_data()
    student_requests_data = main_service.get_all_male_student_requests_data()
    weights = get_weight()
    return jsonify({
        "success": True,
        "message": "Successfully fetched all rooms and male student requests.",
        "rooms": rooms_data,
        "student_requests": student_requests_data,
        "weights": {
            "academic_year": weights[2],
            "major": weights[8],
            "social_style": weights[1],
            "bedtime_habit": weights[0],
            "religion": weights[7],
            "average_monthly_spending": weights[6],
            "is_smoker": weights[9],
            "sports_passion": weights[3],
            "music_passion": weights[4],
            "gaming_passion": weights[5],
        }
    }), 200

@main_api.route("/labeled_data", methods=["POST"])
def save_labeled_data():
    main_service = MainService()
    data = json.loads(request.get_data().decode("utf-8"))
    main_service.save_labeled_data(*data)
    re_calculate_weights()
    return jsonify({
        "success": True,
        "message": "Successfully save all labeled data."
    }), 200
    
@main_api.route("/k-means-result", methods=["GET"])
def get_k_means_result():
    main_service = MainService()
    male_student_requests_data = main_service.get_all_male_student_requests_data()
    data_frame = pd.DataFrame(male_student_requests_data)
    num_rooms = len(main_service.get_all_rooms_data())
    result = kmeans(data_frame, num_rooms, get_weight(), max_iter = num_rooms*2)
    k_means_result = main_service.save_k_means_result(result)
    return jsonify({
        "success": True,
        "message": "Successfully fetched K-means result.",
        "id": k_means_result.id,
        "result": result
    }), 200
    
@main_api.route("/allocation-result", methods=["GET"])
def get_allocation_result():
    k_means_result_id = request.args.get("id", None)
    
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
        
    allocation_result = solver(k_means_result)
    return jsonify({
        "success": True,
        "message": "Successfully fetched allocation result.",
        "result": allocation_result
    }), 200
