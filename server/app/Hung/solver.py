
import random as rd

from ..services.main_service import MainService
from ..k_means_handler.distance import euclidean_distance_with_weights_2
from .kmean import handle_kmean_result, kmean
from .backtracking import backtracking, interger_programing, greedy
from .weight import get_weight
from .metric import mean_euclid_distance_of_room

main_service = MainService()

def solver(kr):
    rooms = main_service.get_all_rooms_data()
    result, remaining_room_ids, remaining_student_ids = handle_kmean_result(kr, rooms)
    INTERGER_PROGRAMING_MAX_NUM_STUDENTS = 18
    while len(remaining_student_ids) > INTERGER_PROGRAMING_MAX_NUM_STUDENTS:
        set_remaining_room_ids = set(remaining_room_ids)
        result2, remaining_room_ids, remaining_student_ids = kmean(
            remaining_student_ids,
            [room for room in rooms if room["id"] in set_remaining_room_ids]
        )
        result += result2

    if len(remaining_student_ids) != 0:
        def pick(n, m, k):
            c = list(set(k))
            def TRY(n, a):
                if n == m: return a.copy(), n
                if n > m: return None, None
                best_r1 = a.copy()
                best_r2 = n
                for i in c:
                    a.append(i)
                    r1, r2 = TRY(n + i, a)
                    if r2 and best_r2 < r2:
                        best_r2 = r2
                        best_r1 = r1
                    a.pop()
                return best_r1, best_r2
            r1, r2 = TRY(n, [])
            if not r1:
                return []
            c = {}
            for i in r1:
                if c.get(i, None): c[i] += 1
                else: c[i] = 1
            r = []
            for i in range(len(k)):
                if c.get(k[i], None):
                    r.append(i)
                    c[k[i]] -= 1
            return r

        room_mapping = { room["id"]: room for room in rooms }
        for r in result:
            r["med"] = mean_euclid_distance_of_room(r["student_ids"], get_weight())
        idx = [i for i in range(len(result))]
        idx.sort(key=lambda i: result[i]["med"], reverse=True)
        result = [result[i] for i in idx]
        idx = pick(len(remaining_student_ids), INTERGER_PROGRAMING_MAX_NUM_STUDENTS, [int(room_mapping[r["room_id"]]["capacity"]) for r in result])

        for i in idx:
            remaining_room_ids.append(result[i]["room_id"])
            remaining_student_ids += result[i]["student_ids"]
        result = [result[i] for i in range(len(result)) if i not in idx]

        set_remaining_room_ids = set(remaining_room_ids)
        room_capacities = {
            room["id"]: int(room["capacity"]) for room in rooms if room["id"] in set_remaining_room_ids
        }
        d = euclidean_distance_with_weights_2(remaining_student_ids, get_weight())
        print(f"Running interger_programing with {len(remaining_student_ids)} students, {len(set_remaining_room_ids)} rooms!")
        result += interger_programing(remaining_student_ids, room_capacities, d, rd.randint(120, 180))

    for r in result:
        if not r.get("med", None):
            r["med"] = mean_euclid_distance_of_room(r["student_ids"], get_weight())
    
    return result

def local_optimization(result):
    if len(result) < 2: return { "does_not_changed": True }

    rooms = main_service.get_all_rooms_data()
    room_mapping = { room["id"]: room for room in rooms }

    result.sort(key=lambda r: r["med"], reverse=True)
    considered = set()
    for c in range(1, len(result)):
        for i in range(c - 1):
            for j in range(i + 1, c):
                if f"{i}-{j}" in considered: continue
                considered.add(f"{i}-{j}")
                r1 = result[i]
                r2 = result[j]

                student_ids = r1["student_ids"] + r2["student_ids"]
                result2 = interger_programing(
                    student_ids,
                    { room_id: int(room_mapping[room_id]["capacity"]) for room_id in [r1["room_id"], r2["room_id"]] },
                    d = euclidean_distance_with_weights_2(student_ids, get_weight())
                )

                for r in result2:
                    r["med"] = mean_euclid_distance_of_room(r["student_ids"], get_weight())

                changed = (r1["med"] + r2["med"] - result2[0]["med"] - result2[1]["med"]) > 0.00000001
                if changed:
                    result[i] = result2[0]
                    result[j] = result2[1]
                    return {
                        "result": result,
                        "does_not_changed": False
                    }
    return {
        "does_not_changed": True
    }
