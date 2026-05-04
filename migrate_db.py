import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Add the current directory to sys.path to ensure 'models' is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import db, User, Book, ReadingProgress, Profile, UserFavorite, ContactUs, UserActivity, UserAchievement, Admin, FriendRequest, ReadingInvite

# Configuration
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
MYSQL_DBNAME = os.getenv('MYSQL_DBNAME', 'Readsmart')

PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', '')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_DBNAME = os.getenv('PG_DBNAME', 'Readsmart')

def migrate():
    # 1. Create Engines
    mysql_uri = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DBNAME}'
    pg_uri = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'
    
    print(f"Connecting to MySQL: {mysql_uri}")
    mysql_engine = create_engine(mysql_uri)
    
    print(f"Connecting to PostgreSQL: {pg_uri}")
    pg_engine = create_engine(pg_uri)
    
    # 2. Create Tables in PostgreSQL
    print("Creating tables in PostgreSQL...")
    from app import app
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")

    # 3. Setup Sessions
    MysqlSession = sessionmaker(bind=mysql_engine)
    mysql_session = MysqlSession()
    
    PgSession = sessionmaker(bind=pg_engine)
    pg_session = PgSession()

    # 4. Define models to migrate (Order matters for foreign keys)
    # Primary tables first
    models = [
        User,
        Admin,
        Book,
        # Dependent tables
        Profile,
        ReadingProgress,
        UserFavorite,
        ContactUs,
        UserActivity,
        UserAchievement,
        FriendRequest,
        ReadingInvite
    ]

    try:
        for model in models:
            table_name = model.__tablename__
            print(f"Migrating table: {table_name}...")
            
            # Fetch all records from MySQL
            records = mysql_session.query(model).all()
            print(f"  Found {len(records)} records.")
            
            # Clear PostgreSQL table before migration (optional, but safer for re-runs)
            pg_session.query(model).delete()
            pg_session.commit()
            
            # Insert into PostgreSQL
            for record in records:
                # Merge into the new session to recreate the object
                pg_session.merge(record)
            
            pg_session.commit()
            print(f"  Successfully migrated {table_name}.")

        print("\nMigration completed successfully!")
        print("Note: If you have auto-incrementing IDs, you might need to reset sequences in PostgreSQL.")
        print("Example: SELECT setval('users_id_seq', (SELECT max(id) FROM users));")

    except Exception as e:
        print(f"\nAn error occurred during migration: {e}")
        pg_session.rollback()
    finally:
        mysql_session.close()
        pg_session.close()

if __name__ == "__main__":
    migrate()
