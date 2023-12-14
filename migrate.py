# migrate.py
from sqlalchemy import create_engine, text

# Replace with your database URI
DATABASE_URI = 'mysql+pymysql://root:%40shish209e@localhost/fuel_db'

engine = create_engine(DATABASE_URI)

with engine.connect() as connection:
    query = text('ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;')
    connection.execute(query)
    print("Migration successful.")
