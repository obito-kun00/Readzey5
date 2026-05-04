from app import app, db
from sqlalchemy import text

def reset_sequences():
    tables = ['users', 'books', 'admin', 'friend_requests', 'reading_invites']
    with app.app_context():
        try:
            for table in tables:
                print(f"Resetting sequence for {table}...")
                db.session.execute(text(f"SELECT setval('{table}_id_seq', (SELECT max(id) FROM {table}))"))
            db.session.commit()
            print("\nAll ID sequences reset successfully!")
        except Exception as e:
            print(f"Error resetting sequences: {e}")
            db.session.rollback()

if __name__ == "__main__":
    reset_sequences()
