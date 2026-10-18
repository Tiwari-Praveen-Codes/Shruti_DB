import os
from seed_100_students import seed_database

def seed_shruti_data():
    seed_database("MySQL")
    seed_database("SQLite")
    return True

if __name__ == "__main__":
    seed_shruti_data()
