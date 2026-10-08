import os
import tempfile
import pytest

from app import app
import app as app_module


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    app_module.DATABASE = db_path

    conn = app_module.get_db()

    conn.execute("""
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            barcode TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)

    if os.path.exists(db_path):
        os.unlink(db_path)
