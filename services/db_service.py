import psycopg2
from psycopg2.extras import RealDictCursor
from config.db_config import db_config

class DatabaseService:
    @staticmethod
    def get_connection():
        return psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )

    @staticmethod
    def execute_query(query, params=None):
        try:
            conn = DatabaseService.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, params or ())
            result = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            return result
        except Exception as e:
            conn.rollback()
            raise e

    @staticmethod
    def execute_single_query(query, params=None):
        try:
            conn = DatabaseService.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query, params or ())
            result = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return result
        except Exception as e:
            conn.rollback()
            raise e 