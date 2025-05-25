#Objective: create a decorator that retries database operations if they fail due to transient errors

import time
import sqlite3
import functools

# === Decorator: Open and close DB connection ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # Adjust DB path as needed
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === Decorator: Retry on failure ===
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[Attempt {attempt}] Trying database operation...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Warning] Attempt {attempt} failed: {e}")
                    last_exception = e
                    if attempt < retries:
                        time.sleep(delay)
            print("[Error] All retry attempts failed.")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# === Attempt to fetch users with retry ===
users = fetch_users_with_retry()
print(users)
