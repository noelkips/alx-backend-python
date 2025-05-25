import time
import sqlite3 
import functools

# === Global cache dictionary ===
query_cache = {}

# === Decorator: open and close DB connection ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # Adjust the DB path as needed
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === Decorator: Cache results based on SQL query string ===
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract the query string from either args or kwargs
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query in query_cache:
            print("[Cache] Returning cached result for query.")
            return query_cache[query]
        else:
            print("[DB] Executing and caching result for query.")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# === First call will cache the result ===
users = fetch_users_with_cache(query="SELECT * FROM users")

# === Second call will use the cached result ===
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users)
