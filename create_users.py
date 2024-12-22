import pandas as pd

# Create initial users DataFrame
initial_users = pd.DataFrame({
    'username': ['admin'],
    'email': ['admin@example.com'],
    'name': ['Admin User'],
    'password': ['$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLxOxs2UfS3LCom']  # password: admin123
})

# Save to Excel
initial_users.to_excel('users.xlsx', index=False)
print("Initial users.xlsx file created successfully!")
