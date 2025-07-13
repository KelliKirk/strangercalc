import psycopg2 
from psycopg2.extras import RealDictCursor
from . import config

class Database:
    """PostgreSQL manager"""

    def __init__(self):
        try:
            self.init_database()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
            raise

    def get_connection(self):
        """Get database connection"""
        try:
            conn = psycopg2.connect(
                host=config.DB_HOST,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                port=config.DB_PORT
            )
            return conn
        except Exception as e:
            print(f"Database connection error: {e}")
            raise

    def init_database(self):
        """Create tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculations (
                id SERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                operation TEXT NOT NULL,
                first_number DECIMAL(15,6),
                second_number DECIMAL(15,6),
                result DECIMAL(15,6),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                last_result DECIMAL(15,6),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                recently_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()

    def save_calculation(self, session_id, operation, first_number, second_number, result):
        """Save calculations to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO calculations (session_id, operation, first_number, second_number, result)
                VALUES (%s, %s, %s, %s, %s)
            ''', (session_id, operation, first_number, second_number, result))
            
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Calculation saved: {operation} {first_number} {second_number} = {result}")
        except Exception as e:
            print(f"Error saving calculation: {e}")
            raise

    def history(self, session_id, limit=10):
        """Calculation history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute('''
                SELECT operation, first_number, second_number, result, date
                FROM calculations
                WHERE session_id = %s
                ORDER BY date DESC 
                LIMIT %s
            ''', (session_id, limit))
            
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            print(f"Retrieved {len(results)} history records for session {session_id}")
            return results
        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []
    
    def save_session(self, session_id, last_result):
        """Save session"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sessions (id, last_result, recently_used)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (id) DO UPDATE SET
                    last_result = EXCLUDED.last_result,
                    recently_used = EXCLUDED.recently_used
            ''', (session_id, last_result))
            
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Session saved: {session_id} with result {last_result}")
        except Exception as e:
            print(f"Error saving session: {e}")
            raise