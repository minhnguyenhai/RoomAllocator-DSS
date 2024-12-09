
import pandas as pd
from ..k_means_handler.k_means_handler import kmeans as _kmeans
from .weight import get_weight
from ..services.main_service import MainService

main_service = MainService()

def kmean(student_ids, rooms):
    df = pd.DataFrame([main_service.get_male_student_request_by_id(id) for id in student_ids])
    return handle_kmean_result(
        _kmeans(df, len(rooms), get_weight()),
        rooms
    )

def handle_kmean_result(kr, rooms):
    student_ids_list = kr[0]
    student_ids_list.sort(key=len, reverse=True)
    print(sum(len(i) for i in student_ids_list), sum(int(i["capacity"]) for i in rooms))
    
    distinct_room_capacities = list(set([r["capacity"] for r in rooms]))
    distinct_room_capacities.sort(key=int)
    room_capacities = [[int(c), [room["id"] for room in rooms if room["capacity"] == c]] for c in distinct_room_capacities]
    print(room_capacities)
    def idx(n):
        if n < room_capacities[0][0]: return -1
        def _idx(n, l, r):
            if r - l < 2:
                if n >= room_capacities[r][0] and len(room_capacities[r][1]) > 0: return r
                if n >= room_capacities[l][0] and len(room_capacities[l][1]) > 0: return l
                return -1
            m = (l + r)//2
            if n >= room_capacities[m][0]:
                t = _idx(n, m, r)
                if t >= 0: return t
            return _idx(n, l, m)
        return _idx(n, 0, len(room_capacities) - 1)

    remaining_student_ids = []
    result = []
    for student_ids in student_ids_list:
        while True:
            n = len(student_ids)
            if n == 0: break
            i = idx(n)
            if i >= 0:
                print(len(student_ids), room_capacities[i][0])
                result.append({
                    "room_id": room_capacities[i][1].pop(),
                    "student_ids": student_ids[-room_capacities[i][0]:]
                })
                student_ids = student_ids[:-room_capacities[i][0]]
            else:
                print(len(student_ids))
                remaining_student_ids += student_ids
                break
    remaining_room_ids = []
    for room_capacity in room_capacities:
        remaining_room_ids += room_capacity[1]
    print(remaining_room_ids, remaining_student_ids)
    
    return result, remaining_room_ids, remaining_student_ids
