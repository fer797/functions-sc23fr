import psycopg2
from psycopg2.extras import execute_batch, DictCursor

class PostgresDB:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connection to PostgreSQL DB successful")
        except Exception as e:
            print(f"Error: {e}")
            self.connection = None
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

    def execute_query(self, query, data):
        if self.connection is None or self.connection.closed:
            self.connect()

        with self.connection.cursor() as cursor:
            execute_batch(cursor, query, data)
            self.connection.commit()

    def fetch_all(self, query):
        if self.connection is None or self.connection.closed:
            self.connect()

        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result