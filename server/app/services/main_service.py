import logging
from .. import db
from ..models.room import Room
from ..models.male_student_request import MaleStudentRequest
from ..models.k_means_result import KMeansResult


class MainService:
    def __init__(self):
        pass
    
    
    def get_male_student_request_by_id(self, student_id):
        student_request = MaleStudentRequest.query.get(student_id)
        if not student_request:
            return None
        return student_request.to_dict()
    
    
    def get_all_rooms_data(self):
        rooms = Room.query.all()
        return [room.to_dict() for room in rooms]
    
    
    def get_all_male_student_requests_data(self):
        student_requests = MaleStudentRequest.query.all()
        return [student_request.to_dict() for student_request in student_requests]
    
    
    def get_k_means_result(self, id):
        k_means_result = KMeansResult.query.get(id)
        if not k_means_result:
            return None
        return k_means_result.result
    
    
    def save_k_means_result(self, result):
        try:
            new_k_means_result = KMeansResult(result=result)
            db.session.add(new_k_means_result)
            db.session.commit()
            return new_k_means_result.to_dict()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while saving K-means result: {e}")
            raise
