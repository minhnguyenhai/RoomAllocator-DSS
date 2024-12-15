import numpy as np
from .vectorize_student import vectorize_student_by_id

# Hàm tính khoảng cách Euclidean giữa 2 sinh viên:
def euclidean_distance_with_weights(id1, id2, weights=[1,1,1,1,1,1,1,1,1,1]):
    """
    Tính khoảng cách Euclidean có áp dụng trọng số.
    
    Args:
        id1 : id sinh viên 1.
        id2 : id sinh viên 2.
        weights (list): Trọng số tương ứng cho mỗi thuộc tính (cùng độ dài với `a` và `b`).
    
    Returns:
        float: Khoảng cách Euclidean có áp dụng trọng số.
    """
    a = vectorize_student_by_id(id1)
    b = vectorize_student_by_id(id2)

    discrete_columns = [7,8,9]
    distance = 0
    for i in range(len(a)):
        if i in discrete_columns:
            # Áp dụng trọng số cho thuộc tính rời rạc
            distance += weights[i] * ((a[i] != b[i])**2)
        else:
            # Áp dụng trọng số cho thuộc tính liên tục
            distance += weights[i] * ((a[i] - b[i]) ** 2)
    return np.sqrt(distance) if distance > 0 else 0

def euclidean_distance_with_weights_2(ids, weights):
    original_vectors = [vectorize_student_by_id(id) for id in ids]

    def split_by_discrete_columns(l):
        discrete_columns = [7,8,9]
        return [l[i] for i in range(len(l)) if i not in discrete_columns], [l[i] for i in range(len(l)) if i in discrete_columns]
    
    w1, w2 = split_by_discrete_columns(weights)
    vt1 = [split_by_discrete_columns(v)[0] for v in original_vectors]
    vt2 = [split_by_discrete_columns(v)[1] for v in original_vectors]
    w1, w2, vt1, vt2 = (np.array(i) for i in (w1, w2, vt1, vt2))
    n = len(ids)

    ds = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            ds[i, j] = np.sum(w2 * (vt2[i] != vt2[j])) + np.sum(w1*((vt1[i] - vt1[j])**2))

    t = np.sqrt(ds).tolist()
    r = {}
    for i in range(len(t)):
        s = {}
        for j in range(len(t[i])):
            s[ids[j]] = t[i][j]
        r[ids[i]] = s

    return r
