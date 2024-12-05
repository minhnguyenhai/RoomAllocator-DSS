import json
import random
from faker import Faker
from app import create_app, db
from app.models.student_request import StudentRequest


def load_names_from_json():
    with open("./data/name_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["first_names"], data["male_last_names"], data["female_last_names"]


faker = Faker()
first_names, male_last_names, female_last_names = load_names_from_json()

genders = ["Nam", "Nữ"]
bed_time_habits = ["Sớm", "Bình thường", "Muộn"]
social_stypes = ["Hướng nội", "Hướng ngoại", "Bình thường"]
religions = ["Có", "Không"]
academic_years = [66, 67, 68, 69]
majors = ["CNTT&TT", "Cơ khí", "Điện - Điện tử", "Kinh tế", "Ngoại ngữ"]
sports_passions = ["Có", "Không", "Bình thường"]
music_passions = ["Có", "Không", "Bình thường"]
gaming_passions = ["Có", "Không", "Bình thường"]


def generate_student_requests_data(num_of_records, seed=42):
    data = []
    faker.seed_instance(42)
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
            bed_time_habit=random.choices(bed_time_habits, [0.15, 0.5, 0.35])[0],
            social_style=random.choices(social_stypes, [0.25, 0.5, 0.25])[0],
            religion=random.choices(religions, [0.2, 0.8])[0],
            academic_year=academic_year,
            major=random.choices(majors, [0.25, 0.2, 0.2, 0.2, 0.15])[0],
            sports_passion=random.choices(sports_passions, [0.5, 0.2, 0.3])[0],
            music_passion=random.choices(music_passions, [0.4, 0.4, 0.2])[0],
            gaming_passion=random.choices(gaming_passions, [0.6, 0.1, 0.3])[0],
            average_monthly_spending=random.randint(1500, 5000)*1000
        )
        data.append(student_request)
        
    return data


def insert_data_into_database(num_of_students=2000):
    app = create_app()
    with app.app_context():
        if StudentRequest.query.first() is None:
            student_requests_data = generate_student_requests_data(num_of_students)
            db.session.bulk_save_objects(student_requests_data)
            db.session.commit()
            print(f"{num_of_students} records of student requests data inserted into database.")
        else:
            print("Data for student requests already exist in the database.")
