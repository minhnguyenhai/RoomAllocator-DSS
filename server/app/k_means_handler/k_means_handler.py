import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Hàm vector hóa sinh viên
def vectorize_students(data_origin):
    # Tạo bản sao của dữ liệu để không ảnh hưởng đến dữ liệu gốc
    data = data_origin.copy()
    
    continuous_features = ["bedtime_habit", "social_style", "academic_year", "sports_passion", 
                           "music_passion", "gaming_passion", 
                           "average_monthly_spending"]
    discrete_features = ["religion", "major", "is_smoker"]

    # Mapping cho 'bedtime_habit' (chuyển thời gian từ '9h' đến '3h' thành dạng số thập phân)
    bedtime_mapping = {
        "21h": 9.0, "21h30": 9.5, "22h": 10.0, "22h30": 10.5, "23h": 11.0,
        "23h30": 11.5, "0h": 12.0, "0h30": 12.5, "1h": 13.0, "1h30": 13.5,
        "2h": 14.0, "2h30": 14.5, "3h": 15.0
    }
    data["bedtime_habit"] = data["bedtime_habit"].map(bedtime_mapping)

    # Mapping cho 'social_style' từ chuỗi sang số
    social_style_mapping = {"Hướng nội": 1, "Bình thường": 2, "Hướng ngoại": 3}
    data["social_style"] = data["social_style"].map(social_style_mapping)

    #Mapping cho passion
    passion_mapping = {"Ghét": 0, "Không thích": 1, "Bình thường": 2, "Thích": 3, "Rất thích": 4}
    data["sports_passion"] = data["sports_passion"].map(passion_mapping)
    data["music_passion"] = data["music_passion"].map(passion_mapping)
    data["gaming_passion"] = data["gaming_passion"].map(passion_mapping)
    
    # Chuẩn hóa các thuộc tính liên tục
    scaler = MinMaxScaler()
    continuous_data = data[continuous_features].values  # Lấy dữ liệu thuộc tính liên tục từ DataFrame
    normalized_continuous_data = scaler.fit_transform(continuous_data)  # Chuẩn hóa theo MinMaxScaler

    # Mã hóa các thuộc tính rời rạc
    label_encoder = LabelEncoder()

    # Mã hóa từng thuộc tính rời rạc
    encoded_discrete_data = np.array([label_encoder.fit_transform(data[feature])
                                      for feature in discrete_features]).T

    # Trả về kết quả kết hợp dữ liệu đã chuẩn hóa và đã mã hóa
    return np.hstack([normalized_continuous_data, encoded_discrete_data])

def euclidean_distance_to_centroid(point, centroid, discrete_columns, weights):
    """
    Tính khoảng cách có trọng số giữa một điểm dữ liệu và centroid.

    Args:
        point (list or np.array): Điểm dữ liệu.
        centroid (list): Centroid của cụm, bao gồm giá trị trung bình cho thuộc tính liên tục và tỷ lệ cho thuộc tính rời rạc.
        discrete_columns (list): Danh sách các chỉ số của thuộc tính rời rạc.
        weights (list or np.array): Trọng số của từng thuộc tính.

    Returns:
        float: Khoảng cách đã tính toán.
    """
    # Tính toán khoảng cách
    distance = 0
    for i in range(len(point)):
        if i in discrete_columns:  # Nếu là thuộc tính rời rạc
            value = int(point[i])  # Giá trị rời rạc của điểm
            proportions = centroid[i]  # Lấy mảng tỷ lệ từ centroid
            distance += weights[i] * ((1 - proportions[value])**2)  # Khoảng cách là 1 - tỷ lệ, có nhân trọng số
        else:  # Nếu là thuộc tính liên tục
            distance += weights[i] * ((point[i] - centroid[i]) ** 2)  # Khoảng cách Euclidean có trọng số

    return np.sqrt(distance)

def assign_centroids(data, clusters, continuous_features, discrete_columns):
    """
    Tính lại centroids cho từng cụm dựa trên dữ liệu.

    Args:
        data (np.array): Dữ liệu đã vector hóa.
        clusters (list): Danh sách các chỉ số dữ liệu trong từng cụm.
        continuous_features (list): Danh sách các chỉ số thuộc tính liên tục.
        discrete_columns (list): Danh sách các chỉ số thuộc tính rời rạc.

    Returns:
        list: Danh sách centroids mới.
    """
    new_centroids = []
    for cluster in clusters:
        if len(cluster) == 0:
            continue

        cluster_data = data[cluster]
        new_centroid = []

        # Thuộc tính liên tục: Tính trung bình
        for i in continuous_features:
            new_centroid.append(np.mean(cluster_data[:, i]))

        # Thuộc tính rời rạc: Lưu tỷ lệ
        for i in discrete_columns:
            values, counts = np.unique(cluster_data[:, i], return_counts=True)
            max_value = int(np.max(data[:, i]))
            proportions = np.zeros(max_value + 1)
            for j, value in enumerate(values):
                proportions[int(value)] = counts[j] / len(cluster_data) 
            new_centroid.append(proportions)

        new_centroids.append(new_centroid)
    return new_centroids

# Hàm so sánh hai centroid
def compare_centroids(centroid1, centroid2):
    for c1, c2 in zip(centroid1, centroid2):
        if isinstance(c1, np.ndarray) and isinstance(c2, np.ndarray):
            # So sánh các mảng numpy
            if not np.array_equal(c1, c2):
                return False
        elif isinstance(c1, np.float64) and isinstance(c2, np.float64):
            # So sánh các giá trị np.float64
            if not np.isclose(c1, c2):
                return False
    return True

def kmeans(datafr, k, weights, max_iter=100):
    # print("datafr", datafr)
    data = vectorize_students(datafr)
    # print("data", data)
    n_samples, n_features = data.shape

    discrete_columns = [7, 8, 9]
    continuous_features = [0, 1, 2, 3, 4, 5, 6]

    # Khởi tạo centroid ban đầu ngẫu nhiên
    centroids = []
    
    indices = np.random.choice(n_samples, k, replace=False)
    for idx in indices:
        point = data[idx].tolist()
        centroid = []
        for i in range(n_features):
            if i in continuous_features:
                centroid.append(point[i])
            elif i in discrete_columns:
                max_value = int(np.max(data[:, i]))
                proportions = np.zeros(max_value + 1)
                proportions[int(point[i])] = 1.0
                centroid.append(proportions)
        centroids.append(centroid)

    unchanged_iterations = 0

    for iteration in range(max_iter):
        clusters = [[] for _ in range(k)]

        # Bước 1: Gán điểm dữ liệu vào cụm gần nhất
        for idx, point in enumerate(data):
            distances = [
                euclidean_distance_to_centroid(point, centroid, discrete_columns, weights)
                for centroid in centroids
            ]
            cluster_idx = np.argmin(distances)
            clusters[cluster_idx].append(idx)

        # Kiểm tra và xử lý cụm trống
        for i in range(k):
            if len(clusters[i]) == 0:
                distances_to_other_centroids = np.array([
                    np.max([
                        euclidean_distance_to_centroid(point, centroid, discrete_columns, weights)
                        for centroid in centroids
                    ]) for point in data
                ])
                new_centroid_idx = np.argmax(distances_to_other_centroids)
                new_centroid_data = data[new_centroid_idx].tolist()
                
                centroid = []
                for j in range(n_features):
                    if j in continuous_features:
                        centroid.append(new_centroid_data[j])
                    elif j in discrete_columns:
                        max_value = int(np.max(data[:, j]))
                        proportions = np.zeros(max_value + 1)
                        proportions[int(new_centroid_data[j])] = 1.0
                        centroid.append(proportions)
                centroids[i] = centroid
                
                # Xóa new_centroid_idx khỏi các cụm khác
                for j in range(k):
                    if new_centroid_idx in clusters[j]:
                        clusters[j].remove(new_centroid_idx)
                
                # Gán điểm này vào cụm trống
                clusters[i] = [new_centroid_idx]


        # Bước 2: Tính lại centroid
        new_centroids = assign_centroids(data, clusters, continuous_features, discrete_columns)

        # Kiểm tra điều kiện dừng
        ui = 0
        for i in range(k):
            ui+=1
            if len(clusters[i]) == 0:
                continue
            if not compare_centroids(centroids[i], new_centroids[i]):
                break
        if ui == k:
            unchanged_iterations += 1
            if unchanged_iterations >= 3:
                break
        else:
            unchanged_iterations = 0

        centroids = new_centroids

    # Tính trung bình bình phương khoảng cách trong từng cụm
    mean_squared_distances = []
    for cluster_idx in range(k):
        if len(clusters[cluster_idx]) == 0:
            mean_squared_distances.append(0)  # Nếu cụm trống, đặt giá trị là 0
        else:
            total_distance = sum(
                euclidean_distance_to_centroid(data[idx], centroids[cluster_idx], discrete_columns, weights)**2
                for idx in clusters[cluster_idx]
            )
            mean_squared_distances.append(total_distance / len(clusters[cluster_idx]))

    # Thay thế chỉ số trong clusters bằng student_id
    clusters_with_student_ids = []
    kkk = 0
    for cluster in clusters:
        cluster_student_ids = datafr.loc[cluster, 'student_id'].tolist()
        clusters_with_student_ids.append(cluster_student_ids)
        print(kkk, cluster_student_ids)
        kkk += 1

    return clusters_with_student_ids, mean_squared_distances