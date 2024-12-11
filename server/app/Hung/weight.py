
import os, json
from ..services.main_service import MainService
from ..k_means_handler.vectorize_student import vectorize_student

main_service = MainService()

def distance(std1, std2):
    a = vectorize_student(std1)
    b = vectorize_student(std2)

    discrete_columns = [7,8,9]
    distance = []
    for i in range(len(a)):
        if i in discrete_columns:
            distance.append((a[i] != b[i])**2)
        else:
            distance.append((a[i] - b[i]) ** 2)
    return distance

_weights = None
def re_calculate_weights():
    global _weights
    def end():
        global _weights
        _weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    dir = os.path.join(os.path.dirname(__file__), "labeled_data")
    if not os.path.exists(dir): return end()
    X = []
    y = []
    files = os.listdir(dir)
    for i in range(len(files)):
        file = os.path.join(dir, files[i])
        if not os.path.isfile(file): continue
        count = 0
        try:
            with open(file, encoding="utf-8") as f:
                data = json.loads(f.read())
            for r in data:
                X.append(distance(r["std1"], r["std2"]))
                y.append(r["dis"]**2)
                count += 1
        except:
            pass
        if count < 10: print(f"File {files[i]} only has {count} records!")
    for r in main_service.get_all_labeled_data():
        X.append(distance(r["std1"], r["std2"]))
        y.append(r["dis"]**2)
    if len(X) == 0: return end()
    from sklearn.linear_model import LinearRegression
    reg = LinearRegression().fit(X, y)
    weights = reg.coef_.tolist()
    if sum(1 if abs(w) > 0.01 else 0 for w in weights) == 0: return end()
    _weights = [max(w, 0) for w in weights]

def get_weight():
    if not _weights:
        re_calculate_weights()
    return _weights
