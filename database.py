from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Check if the environment variable is set and get its value
pgsql_data = os.getenv('DB_CONNECTION_STRING')

# Create the SQLAlchemy engine
engine = create_engine(pgsql_data)

def load_mystery_from_db():
    # Establish a connection to the database
    with engine.connect() as conn:
        print("Connection with database is successful")

        # Execute SQL query to fetch data from the 'mysteries' table
        result = conn.execute(text("SELECT * FROM mysteries"))
        
        # Initialize an empty list to store the query results
        result_dict = []
        
        # Iterate over each row in the query result
        for row in result.all():
            # Construct a dictionary for each row and append it to the result list
            result_dict.append({
                "mystery_id": row[0],
                "mystery_title": row[1],
                "mystery_english": row[2],
                "mystery_hinglish": row[3],
                "mystery_hindi": row[4],
                "mystery_marathi": row[5],
                "mystery_hint_english": row[6],
                "mystery_hint_hinglish": row[7],
                "mystery_hint_hindi": row[8],
                "mystery_hint_marathi": row[9],
                "mystery_solution_english": row[10],
                "mystery_solution_hinglish": row[11],
                "mystery_solution_hindi": row[12],
                "mystery_solution_marathi": row[13]
            })
        
        # Return the list of dictionaries containing the fetched data
        return result_dict