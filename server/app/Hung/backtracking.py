
import random as rd

_best_score = {}
_best_result = {}
def backtracking(student_ids, room_capacities, d):
    global _best_result
    id = rd.randint(1, 10e10)
    def TRY(id, index = 0, student_ids_in_rooms = {}):
        global _best_score, _best_result
        if index == len(student_ids):
            score = sum(
                sum(
                    sum(d[id1][id2]**3 for id2 in room_student_ids) for id1 in room_student_ids
                )**1/3
                for room_student_ids in student_ids_in_rooms.values()
            )
            if score < _best_score.get(id, 10e10):
                _best_score[id] = score
                _best_result[id] = [
                    {
                        "room_id": a,
                        "student_ids": b.copy()
                    }
                    for a, b in student_ids_in_rooms.items()
                ]
            return

        if len(student_ids_in_rooms) == 0:
            student_ids_in_rooms = {
                room_id: [] for room_id in room_capacities
            }
        
        for room_id, room_student_ids in student_ids_in_rooms.items():
            if len(room_student_ids) >= room_capacities[room_id]:
                continue
            room_student_ids.append(student_ids[index])
            TRY(id, index + 1, student_ids_in_rooms)
            room_student_ids.pop()
    
    TRY(id)

    result = _best_result.get(id, None)
    _best_result.pop(id, None)
    _best_score.pop(id, None)

    return result
