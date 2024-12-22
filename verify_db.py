# verify_db.py
import pandas as pd
import os

def check_database():
    if os.path.exists('users.xlsx'):
        df = pd.read_excel('users.xlsx')
        print("\nDatabase Status:")
        print("----------------")
        print(f"Total users: {len(df)}")
        print("\nRegistered usernames:")
        for idx, user in df.iterrows():
            print(f"{idx + 1}. {user['username']}")
            print(f"   Password hash length: {len(user['password'])}")
    else:
        print("users.xlsx not found!")

if __name__ == "__main__":
    check_database()
