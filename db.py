""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import os

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    pool = ThreadedConnectionPool(1, 10, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def add_person (name):
    # Since we're using connection pooling, it's not as big of a deal to have
    # lots of short-lived cursors (I think -- worth testing if we ever go big)
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO person (name) values (%s)", (name,))

def add_fact(source, fact):
	with get_db_cursor(True) as cur:
		cur.execute("INSERT INTO facts (source, fact) values (%s, %s)", (source, fact))

def get_random_fact():
	with get_db_cursor(True) as cur:
		cur.execute("select * from facts order by random() limit 1;")
		return cur.fetchone()

def get_people(page = 0, people_per_page = 10):
    ''' note -- result can be used as list of dictionaries'''
    limit = people_per_page
    offset = page*people_per_page
    with get_db_cursor() as cur:
        cur.execute("select * from person order by person_id limit %s offset %s", (limit, offset))
        return cur.fetchall()

def create_table():
	with get_db_cursor(True) as cur:
		cur.execute("create table facts ( id serial primary key, source text, fact text);")



if __name__ == "__main__":
	print("database url", os.environ['DATABASE_URL'])
	setup()
