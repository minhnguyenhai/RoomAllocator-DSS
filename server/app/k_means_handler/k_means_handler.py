import numpy as np
# from app.utils.vectorizer import vectorize_students

from sklearn.preprocessing import MinMaxScaler, LabelEncoder
# import numpy as np

import pandas as pd

# Hàm vector hóa sinh viên
def vectorize_students(data):
    continuous_features = ["bedtime_habit", "social_style", "sports_passion_score", 
                           "music_passion_score", "gaming_passion_score", 
                           "average_monthly_spending"]
    
    # Mapping cho 'bedtime_habit' (chuyển thời gian từ '9h' đến '3h' thành dạng số thập phân)
    bedtime_mapping = {
        "9h": 9.0, "9h30": 9.5, "10h": 10.0, "10h30": 10.5, "11h": 11.0,
        "11h30": 11.5, "12h": 12.0, "12h30": 12.5, "1h": 13.0, "1h30": 13.5,
        "2h": 14.0, "2h30": 14.5, "3h": 15.0
    }
    
    # Áp dụng mapping cho 'bedtime_habit'
    data["bedtime_habit"] = data["bedtime_habit"].map(bedtime_mapping)
    
    # Mapping cho 'social_style' từ chuỗi sang số
    social_style_mapping = {"Hướng nội": 1, "Bình thường": 2, "Hướng ngoại": 3}
    data["social_style"] = data["social_style"].map(social_style_mapping)
    
    # Chuẩn hóa các thuộc tính liên tục
    scaler = MinMaxScaler()
    continuous_data = data[continuous_features].values  # Lấy dữ liệu thuộc tính liên tục từ DataFrame
    normalized_continuous_data = scaler.fit_transform(continuous_data)  # Chuẩn hóa theo MinMaxScaler
    
    # Mã hóa các thuộc tính rời rạc
    label_encoder = LabelEncoder()
    discrete_features = ["religion", "major", "is_smoker"]
    
    # Mã hóa từng thuộc tính rời rạc
    encoded_discrete_data = np.array([label_encoder.fit_transform(data[feature])
                                      for feature in discrete_features]).T
    
    # Trả về kết quả kết hợp dữ liệu đã chuẩn hóa và đã mã hóa
    return np.hstack([normalized_continuous_data, encoded_discrete_data])

# # Hàm tính khoảng cách Euclidean
# def euclidean_distance_with_weights(a, b, discrete_columns, weights):
#     """
#     Tính khoảng cách Euclidean có áp dụng trọng số.
    
#     Args:
#         a (list): Vector đầu tiên (dữ liệu của sinh viên thứ nhất).
#         b (list): Vector thứ hai (dữ liệu của sinh viên thứ hai).
#         discrete_columns (list): Danh sách các chỉ số (index) của các thuộc tính rời rạc.
#         weights (list): Trọng số tương ứng cho mỗi thuộc tính (cùng độ dài với `a` và `b`).
    
#     Returns:
#         float: Khoảng cách Euclidean có áp dụng trọng số.
#     """
#     distance = 0
#     for i in range(len(a)):
#         if i in discrete_columns:
#             # Áp dụng trọng số cho thuộc tính rời rạc
#             distance += weights[i] * (a[i] != b[i])
#         else:
#             # Áp dụng trọng số cho thuộc tính liên tục
#             distance += weights[i] * ((a[i] - b[i]) ** 2)
#     return np.sqrt(distance)

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

    Raises:
        ValueError: Nếu các tham số đầu vào không hợp lệ.
    """
    # Kiểm tra tính hợp lệ của các tham số đầu vào
    
    # 1. Kiểm tra chiều dài của các mảng
    if not (len(point) == len(centroid) == len(weights)):
        raise ValueError(f"Độ dài của point ({len(point)}), centroid ({len(centroid)}), và weights ({len(weights)}) phải bằng nhau.")
    
    # 2. Kiểm tra tính hợp lệ của discrete_columns
    if not all(0 <= col < len(point) for col in discrete_columns):
        raise ValueError("Các chỉ số cột rời rạc phải nằm trong phạm vi của point.")
    
    # 3. Kiểm tra trọng số
    if not all(weight >= 0 for weight in weights):
        raise ValueError("Tất cả các trọng số phải không âm.")
    
    # 4. Kiểm tra tính hợp lệ của các giá trị rời rạc
    for i in discrete_columns:
        # Kiểm tra xem giá trị của point có phải là số nguyên không
        try:
            value = int(point[i])
        except (ValueError, TypeError):
            raise ValueError(f"Giá trị rời rạc tại vị trí {i} phải là số nguyên.")
        
        # Kiểm tra tính hợp lệ của tỷ lệ trong centroid
        if not isinstance(centroid[i], (list, np.ndarray)):
            raise ValueError(f"Centroid cho thuộc tính rời rạc tại vị trí {i} phải là mảng tỷ lệ.")
        
        # Kiểm tra tổng tỷ lệ bằng 1 (với sai số nhỏ)
        if not np.isclose(sum(centroid[i]), 1.0, atol=1e-5):
            raise ValueError(f"Tổng tỷ lệ tại vị trí {i} phải bằng 1.")
        
        # Kiểm tra giá trị value có nằm trong phạm vi của centroid không
        if value < 0 or value >= len(centroid[i]):
            raise ValueError(f"Giá trị {value} tại vị trí {i} nằm ngoài phạm vi tỷ lệ.")

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

# Hàm K-Means
def kmeans(data, k, discrete_columns, weights, continuous_features, max_iter=100, random_state=None):
    """
    K-Means clustering với hỗ trợ đầy đủ.

    Args:
        data (np.array): Dữ liệu đầu vào đã được vector hóa.
        k (int): Số cụm.
        discrete_columns (list): Danh sách các chỉ số của thuộc tính rời rạc.
        weights (list): Trọng số cho từng thuộc tính.
        continuous_features (list): Danh sách các thuộc tính liên tục.
        max_iter (int): Số vòng lặp tối đa.
        random_state (int, optional): Seed để tái tạo kết quả.

    Returns:
        dict: Từ điển chứa clusters, centroids, và thông tin bổ sung.
    """
    # Đặt seed để tái tạo kết quả
    if random_state is not None:
        np.random.seed(random_state)

    n_samples, n_features = data.shape
    
    # Khởi tạo centroid ban đầu bằng thuật toán K-Means++
    centroids = []
    for _ in range(k):
        # Chọn một điểm ngẫu nhiên
        point = data[np.random.choice(n_samples)].tolist()
        
        # Tạo centroid với các thuộc tính liên tục và rời rạc
        centroid = []
        for i in range(n_features):
            if i in continuous_features:
                # Đối với thuộc tính liên tục, giữ nguyên giá trị
                centroid.append(point[i])
            elif i in discrete_columns:
                # Đối với thuộc tính rời rạc, tạo mảng tỷ lệ
                max_value = int(np.max(data[:, i]))
                proportions = np.zeros(max_value + 1)
                proportions[int(point[i])] = 1.0
                centroid.append(proportions)
            
        centroids.append(centroid)

    # Theo dõi số lần không đổi
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
                # Chọn điểm xa nhất làm centroid mới
                distances_to_other_centroids = np.array([
                    np.max([
                        euclidean_distance_to_centroid(point, centroid, discrete_columns, weights)
                        for centroid in centroids
                    ]) for point in data
                ])
                new_centroid_idx = np.argmax(distances_to_other_centroids)
                new_cen = data[new_centroid_idx].tolist()

                # Tạo centroid với các thuộc tính liên tục và rời rạc
                new_centroid = []
                for i in range(n_features):
                    if i in continuous_features:
                        # Đối với thuộc tính liên tục, giữ nguyên giá trị
                        new_centroid.append(new_cen[i])
                    elif i in discrete_columns:
                        # Đối với thuộc tính rời rạc, tạo mảng tỷ lệ
                        max_value = int(np.max(data[:, i]))
                        proportions = np.zeros(max_value + 1)
                        proportions[int(new_cen[i])] = 1.0
                        new_centroid.append(proportions)
                centroids[i] = new_centroid
                clusters[i] = [new_centroid_idx]

        # Bước 2: Tính lại centroid
        new_centroids = []
        for cluster in clusters:
            if len(cluster) == 0:
                continue
            
            cluster_data = data[cluster]
            new_centroid = []

            # Thuộc tính liên tục: Lấy trung bình
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

        # Kiểm tra điều kiện dừng
        if compare_centroids(centroids, new_centroids):
            unchanged_iterations += 1
            if unchanged_iterations >= 3:  # Dừng nếu ổn định 3 lần liên tiếp
                break
        else:
            unchanged_iterations = 0
        
        centroids = new_centroids

    # Tính toán độ đo chất lượng cụm (ví dụ: within-cluster sum of squares)
    wcss = sum(
        sum(
            euclidean_distance_to_centroid(data[idx], centroids[cluster_idx], discrete_columns, weights)**2
            for idx in clusters[cluster_idx]
        )
        for cluster_idx in range(k)
    )

    return {
        'clusters': clusters,
        'centroids': centroids,
        'wcss': wcss,
        'iterations': iteration + 1
    }
