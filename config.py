# config.py
import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).parent

# Database settings
DATABASE_FILE = BASE_DIR / "data" / "users.xlsx"

# Ensure data directory exists
os.makedirs(BASE_DIR / "data", exist_ok=True)

# Authentication settings
PASSWORD_MIN_LENGTH = 6
USERNAME_MIN_LENGTH = 3
USERID_MIN_LENGTH = 4
USERID_MAX_LENGTH = 15

# Session state keys
SESSION_AUTH_KEY = 'authenticated'
SESSION_USERNAME_KEY = 'username'
SESSION_USERID_KEY = 'user_id'
