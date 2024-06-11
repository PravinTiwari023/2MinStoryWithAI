from sqlalchemy import create_engine, Column, String, Integer, text, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the PostgreSQL connection string from the environment variables
pgsql_data = os.getenv('DB_CONNECTION_STRING')

# Create the SQLAlchemy engine with the given connection string
engine = create_engine(pgsql_data, echo=True)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Declare a base class for models using the ORM
Base = declarative_base()

# Define the 'Suspect' model
class Suspect(Base):
    __tablename__ = 'suspect'
    id = Column(Integer, primary_key=True)
    vote_value = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

# Define the 'Feedback' model
class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    feedback = Column(String(1024), nullable=False)

# Initialize the database and create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Function to save a vote to the database
def save_vote_to_db(vote_value, email):
    session = Session()  # Create a new session
    new_vote = Suspect(vote_value=vote_value, email=email)
    session.add(new_vote)
    try:
        session.commit()  # Commit the transaction
        print(f"Vote for {vote_value} by {email} recorded successfully.")
    except IntegrityError as e:
        session.rollback()  # Rollback in case of an error
        print(f"Database error: {e}")
        raise
    except Exception as e:
        session.rollback()  # Rollback in case of a general exception
        print(f"An error occurred: {e}")
        raise
    finally:
        session.close()  # Close the session

# Function to save feedback to the database
def save_feedback_to_db(name, email, feedback):
    session = Session()  # Create a new session
    new_feedback = Feedback(name=name, email=email, feedback=feedback)
    session.add(new_feedback)
    try:
        session.commit()  # Commit the transaction
        print(f"Feedback from {name} ({email}) recorded successfully.")
    except Exception as e:
        session.rollback()  # Rollback in case of a general exception
        print(f"An error occurred: {e}")
        raise
    finally:
        session.close()  # Close the session

# Function to collect vote counts from the database
def collect_vote_counts():
    session = Session()  # Create a new session
    try:
        # Query to count votes grouped by vote_value
        results = session.query(Suspect.vote_value, func.count(Suspect.vote_value)).group_by(Suspect.vote_value).all()
        
        # Convert the results to a dictionary
        vote_counts = {vote_value: count for vote_value, count in results}
        return vote_counts
    except Exception as e:
        print(f"An error occurred while collecting vote counts: {e}")
        raise
    finally:
        session.close()  # Close the session

# Function to load mysteries from the database
def load_mystery_from_db():
    with engine.connect() as conn:
        print("Connection with database is successful")

        # Execute SQL query to fetch data from the 'mysteries' table
        result = conn.execute(text("SELECT * FROM mysteries"))
        
        result_dict = []  # Initialize an empty list to store the query results
        
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

# Ensure the database connection string is loaded and secure
if not pgsql_data:
    raise ValueError("Database connection string is not set. Please set the DB_CONNECTION_STRING environment variable.")
