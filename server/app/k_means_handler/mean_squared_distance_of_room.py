from .vectorize_student import vectorize_student_by_id
import numpy as np
from .k_means_handler import euclidean_distance_to_centroid

def mean_squared_distance_of_room(room_member_ids, weights):
    discrete_columns = [7,8,9]
    continuous_features = [0,1,2,3,4,5,6]
    discrete_max_values = [9, 9, 2]
    #vectorize student in room
    room_student_vectors = []
    for student_id in room_member_ids:
        student_vector = vectorize_student_by_id(student_id)
        room_student_vectors.append(student_vector)
    room_student_vectors = np.array(room_student_vectors)

    #find centroid of room
    room_centroid = []
    # Thuộc tính liên tục: Tính trung bình
    for i in continuous_features:
        room_centroid.append(np.mean(room_student_vectors[:, i]))
    # Thuộc tính rời rạc: Lưu tỷ lệ
    for i in discrete_columns:
        values, counts = np.unique(room_student_vectors[:, i], return_counts=True)
        proportions = np.zeros(discrete_max_values[i-7])
        for j, value in enumerate(values):
            proportions[int(value)] = counts[j] / len(room_student_vectors) 
        room_centroid.append(proportions)

    #calculate mean squared distance of room
    total_distance = sum(
                euclidean_distance_to_centroid(point, room_centroid, discrete_columns, weights)**2
                for point in room_student_vectors
            )
    return total_distance/len(room_student_vectors)