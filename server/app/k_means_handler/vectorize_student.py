# Hàm vector hóa 1 sv dựa vào id
def vectorize_student_by_id(id):
    student_info = databasequery(id)
    return vectorize_student(student_info)


# Hàm vector hóa 1 sinh viên
def vectorize_student(student):
    """
    Vector hóa thông tin của một sinh viên thành vector 10 chiều.
    """
    # Mapping cho các giá trị
    bedtime_mapping = {
        "21h": 0, "21h30": 1/12, "22h": 2/12, "22h30": 3/12, "23h": 4/12,
        "23h30": 5/12, "0h": 6/12, "0h30": 7/12, "1h": 8/12, "1h30": 9/12,
        "2h": 10/12, "2h30": 11/12, "3h": 1
    }
    social_style_mapping = {"Hướng nội": 0, "Bình thường": 0.5, "Hướng ngoại": 1}
    academic_year_mapping = {66: 0, 67: 1/3, 68: 2/3, 69: 1}
    sports_passion_mapping = {"Ghét": 0, "Không thích": 0.25, "Bình thường": 0.5, "Thích": 0.75, "Rất thích": 1}
    music_passion_mapping = {"Ghét": 0, "Không thích": 0.25, "Bình thường": 0.5, "Thích": 0.75, "Rất thích": 1}
    gaming_passion_mapping = {"Ghét": 0, "Không thích": 0.25, "Bình thường": 0.5, "Thích": 0.75, "Rất thích": 1}
    religion_mapping = {
        "Không": 0, "Kitô giáo": 0.125, "Công giáo": 0.25, "Tin lành": 0.375, "Phật giáo": 0.5,
        "Hòa Hảo": 0.625, "Cao Đài": 0.75, "Hồi giáo": 0.875, "Khác": 1
    }
    major_mapping = {
        "CNTT & TT": 0, "Cơ khí": 0.125, "Điện - Điện tử": 0.25, "Kinh tế": 0.375,
        "Hóa & KH sự sống": 0.5, "Vật liệu": 0.625, "Toán-Tin": 0.75,
        "Vật lý Kỹ thuật": 0.875, "Ngoại ngữ": 1
    }
    
    is_smoker_mapping = {"Không": 0, "Có": 1}
    
    # Vector hóa từng thuộc tính
    bedtime_habit = bedtime_mapping.get(student.get("bedtime_habit", "21h"), 0)
    social_style = social_style_mapping.get(student.get("social_style", "Bình thường"), 0.5)
    academic_year = academic_year_mapping.get(student.get("academic_year", 66), 0)
    sports_passion_score = sports_passion_mapping.get(student.get("sports_passion_score", "Bình thường"), 0.5)
    music_passion_score = music_passion_mapping.get(student.get("music_passion_score", "Bình thường"), 0.5)
    gaming_passion_score = gaming_passion_mapping.get(student.get("gaming_passion_score", "Bình thường"), 0.5)
    average_monthly_spending = (student.get("average_monthly_spending", 2000) - 2000) / 3000
    religion = religion_mapping.get(student.get("religion", "Không"), 0)
    major = major_mapping.get(student.get("major", "CNTT & TT"), 0)
    is_smoker = is_smoker_mapping.get(student.get("is_smoker", "Không"), 0)
    
    # Trả về vector
    return [
        bedtime_habit, social_style, academic_year, sports_passion_score,
        music_passion_score, gaming_passion_score, average_monthly_spending,
        religion, major, is_smoker
    ]

