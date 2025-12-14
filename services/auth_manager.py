from typing import Optional
from models.user import User
from services.database_manager import DatabaseManager
import bcrypt 

class BcryptHasher:
    """Use bcrypt for secure password hasing and checking"""
    @staticmethod
    def hash_password(plain: str) -> str:
        hashed_bytes = bcrypt.hashpw(
            plain.encode('utf-8'),
            bcrypt.gensalt()
        )
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def check_password(plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(
            plain.encode('utf-8'),
            hashed.encode('utf-8')
        )

class AuthManager:
    """Handles user registration and login."""
    def __init__(self, db: DatabaseManager):
        self._db = db

    def register_user(self, username: str, password: str, role: str = "user"):
        password_hash = BcryptHasher.hash_password(password)
        # ... inserts the correct hash
        self._db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
            (username, password_hash, role),
        )

    def login_user(self, username: str, password: str) -> Optional[User]:
        row = self._db.fetch_one(
        "SELECT username, password_hash, role FROM users WHERE username = ?",
        (username,),
    )
        if row is None:
         return None

        username_db, password_hash_db, role_db = row

        if not password_hash_db.startswith("$2"):
          return None

        if BcryptHasher.check_password(password, password_hash_db):
             return User(username_db, password_hash_db, role_db)

        return None


    def user_exists(self, username: str) -> bool:
        """Check if a user with the given username exists in the database."""
        row = self._db.fetch_one(
            "SELECT username FROM users WHERE username = ?",
            (username,),
        )
        return row is not None
