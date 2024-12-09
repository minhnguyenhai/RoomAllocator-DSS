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
    return np.sqrt(distance)
