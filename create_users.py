# File: create_users.py
import pandas as pd
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Create initial users DataFrame
initial_users = pd.DataFrame({
    'username': ['admin'],
    'email': ['admin@example.com'],
    'name': ['Admin User'],
    'password': [hash_password('admin123')]  # This will create a fresh hash
})

# Save to Excel
initial_users.to_excel('users.xlsx', index=False)
print("Initial users.xlsx file created successfully!")
