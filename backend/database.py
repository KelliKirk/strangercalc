import psycopg2 
from psycopg2.extras import RealDictCursor
from .config import Config

class Database:
    """PostgreSQL manager"""

    def __init__(self):
        self.config = Config()
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(
            host=self.config.DB_HOST,
            database=self.config.DB_NAME,
            user=self.config.DB_USER,
            password=self.config.DB_PASSWORD,
            port=self.config.DB_PORT
        )

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
        conn.close()

    def save_calculation(self, session_id, operation, first_number, second_number, result):
        """Save calculations to database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO calculations (session_id, operation, first_number, second_number, result)
            VALUES (%s, %s, %s, %s, %s)
        ''', (session_id, operation, first_number, second_number, result))
        
        conn.commit()
        conn.close()

    def history(self, session_id, limit=10):
        """Calculation history"""
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
        conn.close()
        return results
    
    def save_session(self, session_id, last_result):
        """Save session"""
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
        conn.close()