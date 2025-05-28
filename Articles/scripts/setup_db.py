import os
from lib.db.connection import get_connection

def setup():
    here = os.path.dirname(__file__)
    schema_path = os.path.join(here, '..', 'lib', 'db', 'schema.sql')
    conn = get_connection()
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.close()
    print("Database schema created.")

if __name__ == '__main__':
    setup()
