import json
import random
from faker import Faker
from app import create_app, db
from app.models.male_student_request import MaleStudentRequest
from app.models.room import Room


def load_names_from_json():
    with open("./data/name_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["first_names"], data["male_last_names"], data["female_last_names"]


faker = Faker()
TOTAL_FLOORS_OF_BUILDING = 5
ROOMS_PER_FLOOR = 10
FIRST_NAMES, MALE_LAST_NAMES, FEMALE_LAST_NAMES = load_names_from_json()

bedtime_habits = ["21h", "21h30", "22h", "22h30", "23h", "23h30", "0h", "0h30", "1h", "1h30", "2h", "2h30", "3h"]
social_stypes = ["Hướng nội", "Hướng ngoại", "Bình thường"]
religions = ["Không", "Kitô giáo", "Công giáo", "Tin lành", "Phật giáo", "Hòa Hảo", "Cao Đài", "Hồi giáo", "Khác"]
academic_years = [66, 67, 68, 69]
majors = ["CNTT & TT", "Cơ khí", "Điện - Điện tử", "Kinh tế", "Hóa & KH sự sống", "Vật liệu", "Toán-Tin", "Vật lý Kỹ thuật", "Ngoại ngữ"]
sports_passions = ["Rất thích", "Thích", "Bình thường", "Không thích", "Ghét"]
music_passions = ["Rất thích", "Thích", "Bình thường", "Không thích", "Ghét"]
gaming_passions = ["Rất thích", "Thích", "Bình thường", "Không thích", "Ghét"]
is_smokers = ["Có", "Không"]


def generate_rooms_data(num_of_records, seed=42):
    random.seed(seed)
    data = []
    total_capacity = 0
    num_of_buildings = num_of_records // (TOTAL_FLOORS_OF_BUILDING * ROOMS_PER_FLOOR)
    
    for building_number in range(3, num_of_buildings+3):
        for floor in range(1, TOTAL_FLOORS_OF_BUILDING+1):
            for room_number in range(1, ROOMS_PER_FLOOR+1):
                room_name = f"B{building_number}-{floor}{room_number:02d}"
                room = Room(
                    building_name=f"B{building_number}",
                    room_name=room_name,
                    capacity=random.choice([6, 8, 10, 12]),
                )
                data.append(room)
                total_capacity += room.capacity
    
    return data, total_capacity


def generate_student_requests_data(num_of_records, seed=42):
    random.seed(seed)
    faker.seed_instance(seed)
    data = []
    
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
        student_request = MaleStudentRequest(
            student_id=student_id,  
            name=f"{random.choice(FIRST_NAMES)} {random.choice(MALE_LAST_NAMES)}",
            bedtime_habit=random.choices(bedtime_habits, [0.01, 0.01, 0.05, 0.05, 0.1, 0.15, 0.2, 0.15, 0.1, 0.05, 0.05, 0.04, 0.04])[0],
            social_style=random.choices(social_stypes, [0.2, 0.5, 0.3])[0],
            religion=random.choices(religions, [0.9, 0.01, 0.03, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])[0],
            academic_year=academic_year,
            major=random.choices(majors, [0.2, 0.14, 0.19, 0.15, 0.14, 0.13, 0.05, 0.05, 0.05])[0],
            sports_passion=random.choices(sports_passions, [0.2, 0.3, 0.3, 0.15, 0.05])[0],
            music_passion=random.choices(music_passions, [0.25, 0.4, 0.3, 0.03, 0.02])[0],
            gaming_passion=random.choices(gaming_passions, [0.3, 0.4, 0.15, 0.1, 0.05])[0],
            average_monthly_spending=random.randint(2000, 5000)*1000,
            is_smoker=random.choices(is_smokers, [0.25, 0.75])[0]
        )
        data.append(student_request)
        
    return data


def insert_data_into_database(num_of_rooms):
    app = create_app()
    with app.app_context():
        if Room.query.first() is None:
            rooms_data, total_capacity = generate_rooms_data(num_of_rooms)
            student_requests_data = generate_student_requests_data(total_capacity)
            db.session.bulk_save_objects(rooms_data)
            db.session.bulk_save_objects(student_requests_data)
            db.session.commit()
            print(f"{num_of_rooms} records of rooms data inserted into the database with a total capacity of {total_capacity} beds.")
            print(f"{total_capacity} records of student requests data inserted into the database.")
        else:
            print(f"Data already exists in the database with {num_of_rooms} rooms.")
