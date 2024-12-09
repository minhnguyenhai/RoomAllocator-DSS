# 🏢 Room Allocator - Decision Support System for Room Distribution

## 🚀 Database Migration & Start Server with Auto Data Insertion

This Flask server automatically inserts data into a PostgreSQL database.

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
