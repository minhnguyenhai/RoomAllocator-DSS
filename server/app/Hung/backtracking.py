
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
                    sum(d[id1][id2] for id2 in room_student_ids) for id1 in room_student_ids
                )/(
                    len(room_student_ids)**2
                )
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

def _greedy(student_ids, room_capacities, d):
    room_ids = list(room_capacities.keys())
    room_ids.sort(key=lambda room_id: room_capacities[room_id], reverse=True)
    room_id_of_student_id: dict[str, str] = { id: None for id in student_ids }
    result = []
    for room_id in room_ids:
        room_student_ids = []
        while len(room_student_ids) < room_capacities[room_id]:
            best_student_id = None
            best_student_score = 10e10
            break_ = False
            for student_id in student_ids:
                if room_id_of_student_id[student_id]: continue
                if len(room_student_ids) == 0:
                    room_id_of_student_id[student_id] = room_id
                    room_student_ids.append(student_id)
                    break_ = True
                    break
                score = sum(d[student_id][id] for id in room_student_ids)
                if score < best_student_score:
                    best_student_score = score
                    best_student_id = student_id
            if break_: continue
            if best_student_id:
                room_student_ids.append(best_student_id)
                room_id_of_student_id[best_student_id] = room_id
            else:
                return None
        result.append({
            "room_id": room_id,
            "student_ids": room_student_ids
        })
    return result

def greedy(student_ids, room_capacities, d):
    best_result = None
    best_score = 10e10
    for i in range(5):
        rd.shuffle(student_ids)
        result = _greedy(student_ids, room_capacities, d)
        if not result: continue
        score = sum(
            sum(
                sum(d[id1][id2]**3 for id2 in r["student_ids"]) for id1 in r["student_ids"]
            )**1/3
            for r in result
        )
        if score < best_score:
            best_score = score
            best_result = result
    return best_result

def interger_programing(student_ids, room_capacities, d, time_limit_seconds = 300):
    from ortools.linear_solver import pywraplp
    solver: pywraplp.Solver = pywraplp.Solver.CreateSolver("SAT")

    room_ids = list(room_capacities.keys())
    original_room_capacities = room_capacities
    room_capacities = [room_capacities[room_id] for room_id in room_ids]
    n_rooms = len(room_ids)
    n_students = len(student_ids)

    x = [[solver.IntVar(0, 1, f"x[{i}][{j}]") for j in range(n_students)] for i in range(n_rooms)]
    y = [[[solver.IntVar(0, 1, f"y[{i}][{j}][{k}]") for k in range(n_students)] for j in range(n_students)] for i in range(n_rooms)]

    for i in range(n_rooms):
        solver.Add(sum(x[i]) == room_capacities[i])
    for j in range(n_students):
        solver.Add(sum(x[i][j] for i in range(n_rooms)) == 1)
    for i in range(n_rooms):
        for j in range(n_students):
            for k in range(n_students):
                solver.Add(y[i][j][k] >= x[i][j] + x[i][k] - 1)
                solver.Add(y[i][j][k] <= (x[i][j] + x[i][k])/2)

    f = sum(
        sum(
            sum(
                y[i][j][k]*d[student_ids[j]][student_ids[k]] for k in range(n_students)
            )
            for j in range(n_students)
        )/(room_capacities[i]**2)
        for i in range(n_rooms)
    )

    solver.Minimize(f)
    if time_limit_seconds:
        solver.SetTimeLimit(time_limit_seconds*1000)
    
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = []
        for i in range(n_rooms):
            result.append({
                "room_id": room_ids[i],
                "student_ids": [student_ids[j] for j in range(n_students) if x[i][j].solution_value() == 1]
            })
        return result
    else:
        print("interger_programing can't find optimal result. Using greedy!")
        return greedy(student_ids, original_room_capacities, d)


def generate_fake_data(n_rooms, n_students_per_room = 12):
    student_ids = ["s" + str(i) for i in range(n_rooms*n_students_per_room)]
    room_capacities = {
        "r" + str(i): n_students_per_room for i in range(n_rooms)
    }
    d = {
        id1: { id2: rd.random()*100 for id2 in student_ids } for id1 in student_ids
    }
    return student_ids, room_capacities, d

def test(f):
    import time
    print("Func:", f.__name__)
    i = 2
    while True:
        for j in range(6, 12 if i == 2 else 13):
            s = time.time()
            f(*generate_fake_data(i, j))
            t = round(time.time() - s)
            print(f"n_rooms = {i}; n_students_per_room = {j}; time = {t}s")
        i += 1

def test2(f1, f2):
    def compare(r1, r2):
        if len(r1) != len(r2): return False
        def handle(r):
            t = [sorted(i["student_ids"]) for i in r]
            t.sort(key=lambda i: i[0])
            return t
        cl1 = handle(r1)
        cl2 = handle(r2)
        for i in range(len(cl1)):
            if ",".join(cl1[i]) != ",".join(cl2[i]):
                return False
        return True
    for i in [2, 3, 4]:
        for j in [3, 4, 5]:
            data = generate_fake_data(i, j)
            print(compare(f1(*data), f2(*data)))
