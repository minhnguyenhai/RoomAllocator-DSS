from app import create_app, db
from data.insert_data import insert_data_into_database

app = create_app()

if __name__ == "__main__":
    insert_data_into_database()
    app.run(host="0.0.0.0", port=5000, debug=True)