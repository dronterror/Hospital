import os
import time
import psycopg2
from urllib.parse import urlparse

def wait_for_db():
    """Wait for database to be available"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise Exception('DATABASE_URL environment variable not set')

    # Parse the database URL
    url = urlparse(db_url)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    max_tries = 60
    while max_tries > 0:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.close()
            print('Database is ready!')
            return
        except psycopg2.OperationalError as e:
            print('Database is not ready. Waiting...')
            max_tries -= 1
            time.sleep(1)

    print('Could not connect to database!')
    exit(1)

if __name__ == '__main__':
    wait_for_db() 