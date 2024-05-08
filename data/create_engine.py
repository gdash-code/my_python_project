from sqlalchemy import create_engine

# Replace 'sqlite:///your_database.db' with your actual database URL
engine = create_engine('sqlite:///your_database.db', echo=True)
