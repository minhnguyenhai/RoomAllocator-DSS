
from ..services.main_service import MainService
from ..k_means_handler.distance import euclidean_distance_with_weights
from .kmean import handle_kmean_result, kmean
from .backtracking import backtracking

main_service = MainService()

def solver(kr):
    rooms = main_service.get_all_rooms_data()
    print("len(kr[0])", sum(len(i) for i in kr[0]))
    # return []
    result, remaining_room_ids, remaining_student_ids = handle_kmean_result(kr, rooms)
    while len(remaining_student_ids) > 15:
        set_remaining_room_ids = set(remaining_room_ids)
        _rooms = [room for room in rooms if room["id"] in set_remaining_room_ids]
        result2, remaining_room_ids, remaining_student_ids = kmean(remaining_student_ids, _rooms)
        result += result2

    if len(remaining_student_ids) != 0:
        set_remaining_room_ids = set(remaining_room_ids)
        d = {
            id1: {
                id2: euclidean_distance_with_weights(id1, id2) if id1 != id2 else 0 for id2 in remaining_student_ids
            } for id1 in remaining_student_ids
        }
        result += backtracking(remaining_student_ids, {
            room["id"]: int(room["capacity"]) for room in rooms if room["id"] in set_remaining_room_ids
        }, d)

    for r in result:
        r["med"] = 1 # ??
    
    return result
