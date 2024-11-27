import json
import random
from faker import Faker
from app import create_app, db
from app.models.dormitory import Dormitory
from app.models.student_request import StudentRequest


fake = Faker()


def load_dormitories_from_json():
    with open("./data/dormitory_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def load_names_from_json():
    with open("./data/name_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["first_names"], data["male_last_names"], data["female_last_names"]


dormitories_data = load_dormitories_from_json()
first_names, male_last_names, female_last_names = load_names_from_json()


def generate_dormitory(dormitory_data):
    return Dormitory(
        building_name=dormitory_data["building_name"],
        total_floors=dormitory_data["total_floors"],
        rooms_per_floor=dormitory_data["rooms_per_floor"],
        rent_per_month=dormitory_data["rent_per_month"],
        people_per_room=dormitory_data["people_per_room"],
        private_toilet=dormitory_data["private_toilet"],
        water_heater=dormitory_data["water_heater"],
        air_conditioner=dormitory_data["air_conditioner"]
    )


def generate_student_request():
    year = random.choice([2021, 2022, 2023])
    random_number = fake.unique.random_number(digits=4)
    student_id = f"{year}{random_number:04d}"
    gender = random.choice(["male", "female"])
    first_name = random.choice(first_names)
    if gender == "male":
        last_name = random.choice(male_last_names)
    else:
        last_name = random.choice(female_last_names)
        
    full_name = f"{first_name} {last_name}"

    return StudentRequest(
        student_id=student_id,  
        name=full_name,
        gender=gender,
        rent_per_month=fake.random_int(min=350000, max=600000),
        people_per_room=fake.random_int(min=6, max=12),
        private_toilet=fake.random_int(min=1, max=2),
        water_heater=fake.random_int(min=0, max=2),
        air_conditioner=fake.random_int(min=0, max=2),
        primary_study_time=fake.random_element(elements=("morning", "afternoon", "evening")),
        social_style=fake.random_element(elements=("introvert", "extrovert", "balanced")),
        silent_space_required=fake.boolean(),
        bed_time_habit=fake.random_element(elements=("early", "late")),
        is_smoker=fake.boolean()
    )


def insert_data_into_database(num_of_students=400):
    app = create_app()
    with app.app_context():
        if Dormitory.query.first() is None:
            dormitories = [generate_dormitory(data) for data in dormitories_data]
            db.session.bulk_save_objects(dormitories)
            db.session.commit()
            print(f"{len(dormitories)} records of dormitories inserted into database.")
        else:
            print("Data for dormitories already exist in the database.")
            
        if StudentRequest.query.first() is None:
            students = [generate_student_request() for _ in range(num_of_students)]
            db.session.bulk_save_objects(students)
            db.session.commit()
            print(f"{num_of_students} records of student requests inserted into database.")
        else:
            print("Data for student requests already exist in the database.")
