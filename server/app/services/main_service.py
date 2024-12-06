import logging
from .. import db
from ..models.dormitory import Dormitory
from ..models.student_request import StudentRequest
from ..models.k_means_result import KMeansResult


class MainService:
    def __init__(self):
        pass
    
    
    def get_all_dormitories_data(self):
        dormitories = Dormitory.query.all()
        return [dormitory.to_dict() for dormitory in dormitories]
    
    
    def get_all_student_requests_data(self):
        student_requests = StudentRequest.query.all()
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
