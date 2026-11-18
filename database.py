
import sqlite3
import json
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "database" / "verification.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_type TEXT,
                extracted_text TEXT,
                extracted_data TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS comparisons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document1_id INTEGER,
                document2_id INTEGER,
                results TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(document1_id) REFERENCES documents(id),
                FOREIGN KEY(document2_id) REFERENCES documents(id)
            )
        """)

        connection.commit()


def save_document(filename, file_type, extracted_text, extracted_data):

    with get_connection() as connection:

        cursor = connection.execute("""
            INSERT INTO documents
            (filename, file_type, extracted_text, extracted_data)
            VALUES (?, ?, ?, ?)
        """, (
            filename,
            file_type,
            extracted_text,
            json.dumps(extracted_data)
        ))

        return cursor.lastrowid


def save_comparison(document1_id, document2_id, results, summary):

    with get_connection() as connection:

        cursor = connection.execute("""
            INSERT INTO comparisons
            (document1_id, document2_id, results, summary)
            VALUES (?, ?, ?, ?)
        """, (
            document1_id,
            document2_id,
            json.dumps(results),
            json.dumps(summary)
        ))

        return cursor.lastrowid


def get_documents():

    with get_connection() as connection:
        return connection.execute("""
            SELECT * FROM documents ORDER BY uploaded_at DESC
        """).fetchall()


def get_comparisons():

    with get_connection() as connection:
        return connection.execute("""
            SELECT * FROM comparisons ORDER BY created_at DESC
        """).fetchall()
