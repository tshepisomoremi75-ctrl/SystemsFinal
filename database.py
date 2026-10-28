import sqlite3
import os

DB_FOLDER = "database"
DB_NAME = os.path.join(DB_FOLDER, "campus.db")


def get_connection():

    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        campus TEXT
    )
    """)

    # RESOURCES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resources(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_code TEXT UNIQUE,
        resource_name TEXT,
        resource_type TEXT,
        campus TEXT,
        availability TEXT
    )
    """)

    # BOOKINGS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lecturer TEXT,
        resource_code TEXT,
        booking_date TEXT,
        start_time TEXT,
        duration INTEGER,
        campus TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_default_resources():

    conn = get_connection()
    cursor = conn.cursor()

    resources = [

        (
            "LAB001",
            "Computer Lab A",
            "Computer Laboratory",
            "Richfield Centurion",
            "Available"
        ),

        (
            "LAB002",
            "Computer Lab B",
            "Computer Laboratory",
            "Richfield Centurion",
            "Available"
        ),

        (
            "PROJ001",
            "Projector 1",
            "Equipment",
            "Richfield Braamfontein",
            "Available"
        ),

        (
            "ROOM001",
            "Seminar Room",
            "Venue",
            "Richfield Polokwane",
            "Available"
        )
    ]

    for resource in resources:

        try:

            cursor.execute("""
            INSERT INTO resources(
                resource_code,
                resource_name,
                resource_type,
                campus,
                availability
            )
            VALUES (?, ?, ?, ?, ?)
            """, resource)

        except:
            pass

    conn.commit()
    conn.close()


# ==========================================
# THIS FUNCTION IS MISSING
# ==========================================

def initialize_database():

    create_tables()
    create_default_resources()