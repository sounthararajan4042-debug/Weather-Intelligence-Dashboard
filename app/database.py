
import sqlite3


DATABASE_NAME = "weather.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL UNIQUE
        )
    """)

    connection.commit()
    connection.close()


def add_search(city):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO search_history (city) VALUES (?)",
        (city,)
    )

    connection.commit()
    connection.close()


def get_history():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, city, searched_at
        FROM search_history
        ORDER BY id DESC
    """)

    history = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return history


def add_favorite(city):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO favorites (city) VALUES (?)",
        (city,)
    )

    connection.commit()
    connection.close()


def remove_favorite(city):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM favorites WHERE city = ?",
        (city,)
    )

    connection.commit()
    connection.close()


def get_favorites():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, city
        FROM favorites
        ORDER BY city
    """)

    favorites = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return favorites
