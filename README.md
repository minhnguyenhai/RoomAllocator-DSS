# 🏢 Room Allocator - Decision Support System for Room Distribution

## 🚀 Database Migration & Start Server with Auto Data Insertion

This Flask server automatically inserts data into a PostgreSQL database. After setting up the database and running migrations, running server auto-inserts **100 records** into the `rooms` table, representing the information of 100 rooms in dormitory with a total capacity of 874 beds, and **874 records** into the `student_requests` table, capturing student dormitory preferences.

1. Create a virtualenv and install the requirements:
```sh
cd server
pip install -r requirements.txt
```

2. Run the database migrations:
```sh
flask db upgrade
```

3. Start server with auto-insert data:
```sh
python3 run.py
```
