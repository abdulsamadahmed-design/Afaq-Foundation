import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "data" / "afaq.db"


def get_connection():
    """Create and return a connection to the Afaq database."""

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def add_missing_project_columns(connection):
    """
    Upgrade an existing projects table with fields
    required by the React frontend.
    """

    columns = connection.execute(
        "PRAGMA table_info(projects)"
    ).fetchall()

    existing_columns = {
        column["name"] for column in columns
    }

    new_columns = {
        "summary": "TEXT NOT NULL DEFAULT ''",
        "beneficiaries": "INTEGER NOT NULL DEFAULT 0",
        "icon": "TEXT NOT NULL DEFAULT '🤝'",
        "goals": "TEXT NOT NULL DEFAULT '[]'",
        "updates": "TEXT NOT NULL DEFAULT '[]'",
    }

    for column_name, definition in new_columns.items():
        if column_name not in existing_columns:
            connection.execute(
                f"""
                ALTER TABLE projects
                ADD COLUMN {column_name} {definition}
                """
            )


def create_tables():
    """Create or upgrade the Afaq database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT,
            role TEXT NOT NULL DEFAULT 'member'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT NOT NULL DEFAULT '',
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            target_amount REAL NOT NULL,
            amount_raised REAL NOT NULL DEFAULT 0,
            beneficiaries INTEGER NOT NULL DEFAULT 0,
            icon TEXT NOT NULL DEFAULT '🤝',
            goals TEXT NOT NULL DEFAULT '[]',
            updates TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'active',
            manager_id INTEGER,
            FOREIGN KEY (manager_id)
                REFERENCES users(id)
        )
    """)

    # Upgrade older databases that already
    # contained the projects table.
    add_missing_project_columns(connection)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            anonymous INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (donor_id)
                REFERENCES users(id),
            FOREIGN KEY (project_id)
                REFERENCES projects(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            event_date TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'upcoming'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'registered',
            FOREIGN KEY (member_id)
                REFERENCES users(id),
            FOREIGN KEY (event_id)
                REFERENCES events(id),
            UNIQUE(member_id, event_id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()

    print(
        f"Afaq database created successfully: "
        f"{DATABASE_PATH}"
    )