import logging
from .. import db
from ..models.room import Room
from ..models.male_student_request import MaleStudentRequest
from ..models.k_means_result import KMeansResult
from ..models.labeled_data import LabledData


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
            return new_k_means_result
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while saving K-means result: {e}")
            raise

    def get_all_labeled_data(self):
        return [labeled_data.json for labeled_data in LabledData.query.all()]
    
    def save_labeled_data(self, *data):
        try:
            db.session.bulk_save_objects([LabledData(json=d) for d in data])
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while saving labeled data: {e}")
            raise
