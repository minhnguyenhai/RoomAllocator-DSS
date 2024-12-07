import json
import random
from faker import Faker
from app import create_app, db
from app.models.student_request import StudentRequest
from app.models.dormitory import Dormitory


def load_dormitories_from_json():
    with open("./data/dormitory_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def load_names_from_json():
    with open("./data/name_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["first_names"], data["male_last_names"], data["female_last_names"]


faker = Faker()
dormitories_info = load_dormitories_from_json()
first_names, male_last_names, female_last_names = load_names_from_json()

genders = ["Nam", "Nữ"]
bedtime_habits = ["21h", "21h30", "22h", "22h30", "23h", "23h30", "0h", "0h30", "1h", "1h30", "2h", "2h30", "3h"]
social_stypes = ["Hướng nội", "Hướng ngoại", "Bình thường"]
religions = ["Không", "Kitô giáo", "Công giáo", "Tin lành", "Phật giáo", "Hòa Hảo", "Cao Đài", "Hồi giáo", "Khác"]
academic_years = [66, 67, 68, 69]
majors = ["CNTT & TT", "Cơ khí", "Điện - Điện tử", "Kinh tế", "Hóa & KH sự sống", "Vật liệu", "Toán-Tin", "Vật lý Kỹ thuật", "Ngoại ngữ"]
is_smokers = ["Có", "Không"]


def generate_dormitories_data():
    data = []
    for dormitory in dormitories_info:
        dormitory_data = Dormitory(
            building_name=dormitory["building_name"],
            total_rooms=dormitory["total_rooms"],
            students_per_room=dormitory["students_per_room"]
        )
        data.append(dormitory_data)
        
    return data


def generate_student_requests_data(num_of_records, seed=42):
    data = []
    faker.seed_instance(seed)
    random.seed(seed)
    
    for _ in range(num_of_records):
        academic_year = random.choices(academic_years, [0.1, 0.2, 0.3, 0.4])[0]
        if academic_year == 66:
            entry_year = 2021
        elif academic_year == 67:
            entry_year = 2022
        elif academic_year == 68:
            entry_year = 2023
        else:
            entry_year = 2024
            
        random_number = faker.unique.random_number(digits=4)
        student_id = f"{entry_year}{random_number:04d}"

        gender = random.choices(genders, [0.6, 0.4])[0]
        first_name = random.choice(first_names)
        if gender == "Nam":
            last_name = random.choice(male_last_names)
        else:
            last_name = random.choice(female_last_names)
            
        full_name = f"{first_name} {last_name}"
        
        student_request = StudentRequest(
            student_id=student_id,  
            name=full_name,
            gender=gender,
            bedtime_habit=random.choices(bedtime_habits, [0.01, 0.01, 0.05, 0.05, 0.1, 0.15, 0.2, 0.15, 0.1, 0.05, 0.05, 0.04, 0.04])[0],
            social_style=random.choices(social_stypes, [0.2, 0.5, 0.3])[0],
            religion=random.choices(religions, [0.4, 0.15, 0.15, 0.15, 0.1, 0.02, 0.01, 0.01, 0.01])[0],
            academic_year=academic_year,
            major=random.choices(majors, [0.2, 0.14, 0.19, 0.15, 0.14, 0.13, 0.05, 0.05, 0.05])[0],
            sports_passion_score=random.randint(1, 10),
            music_passion_score=random.randint(1, 10),
            gaming_passion_score=random.randint(1, 10),
            average_monthly_spending=random.randint(2000, 5000)*1000,
            is_smoker=random.choices(is_smokers, [0.25, 0.75])[0]
        )
        data.append(student_request)
        
    return data


def insert_data_into_database(num_of_students=2000):
    app = create_app()
    with app.app_context():
        if Dormitory.query.first() is None:
            dormitories_data = generate_dormitories_data()
            db.session.bulk_save_objects(dormitories_data)
            db.session.commit()
            print(f"{len(dormitories_data)} records of dormitories data inserted into database.")
        else:
            print("Data for dormitories already exist in the database.")
            
        if StudentRequest.query.first() is None:
            student_requests_data = generate_student_requests_data(num_of_students)
            db.session.bulk_save_objects(student_requests_data)
            db.session.commit()
            print(f"{num_of_students} records of student requests data inserted into database.")
        else:
            print("Data for student requests already exist in the database.")
