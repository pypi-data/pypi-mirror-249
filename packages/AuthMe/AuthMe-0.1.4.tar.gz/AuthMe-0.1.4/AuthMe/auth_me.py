import jwt
import psycopg2
import hashlib
import datetime

from types import SimpleNamespace
from psycopg2 import sql

class AuthMe:
    def __init__(self, db_config, secret_key):
        self.db_config = db_config
        self.secret_key = secret_key

    def initialize_database(self):
        conn, cursor = self._connect_db()
        create_tables_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(256) NOT NULL,
                encrypted_password VARCHAR(256) NOT NULL,
                first_name VARCHAR(256),
                last_name VARCHAR(256),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                reset_password_token VARCHAR(256),
                reset_password_sent_at TIMESTAMP,
                reset_password_at TIMESTAMP,
                active BOOLEAN DEFAULT true NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tokens (
                id SERIAL PRIMARY KEY,
                token VARCHAR(256) NOT NULL,
                user_id INT NOT NULL,
                origin VARCHAR(256) NOT NULL,
                ip_address VARCHAR(256) NOT NULL,
                expiry TIMESTAMP NOT NULL,
                revoked_at TIMESTAMP
            );
        """)

        # execute query
        cursor.execute(create_tables_query)

        # close connection
        self._disconnect_db(conn, cursor)

    def signup(self, user_attributes, origin, ip_address):
        # hash password
        user_attributes['encrypted_password'] = hashlib.sha256(user_attributes['password'].encode()).hexdigest()
        del user_attributes['password']

        # connect to database
        conn, cursor = self._connect_db()

        # check existing user
        if self._check_existing_user(repr(user_attributes['email'])):
            return self._response_user_already_exists()
    
        # signup user
        columns = ', '.join(user_attributes.keys())
        values = '({})'.format(', '.join(map(repr, list(user_attributes.values()))))
        insert_query = f"INSERT INTO users ({columns}) VALUES {values} RETURNING id"
        cursor.execute(insert_query)
        user_id = cursor.fetchone()[0]
        self._disconnect_db(conn, cursor)
        return self._generate_token(user_id, origin, ip_address)
    
    def login(self, email, password, origin, ip_address):
        # hash password
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        # connect to database
        conn, cursor = self._connect_db()

        # check credentials
        credentials_check_query = f"SELECT * FROM users WHERE email = {repr(email)} AND encrypted_password = {repr(encrypted_password)} AND active = true"
        cursor.execute(credentials_check_query)
        user = cursor.fetchone()
        self._disconnect_db(conn, cursor)

        # return error if credentials are invalid
        if not user:
            return self._response_invalid_credentials()
        
        # generate token
        return self._generate_token(user[0], origin, ip_address)
    
    def logout(self, token):
        conn, cursor = self._connect_db()
        revoke_query = f"UPDATE tokens SET revoked_at = CURRENT_TIMESTAMP WHERE token = {repr(token)} AND revoked_at IS NULL"
        cursor.execute(revoke_query)
        self._disconnect_db(conn, cursor)
        response = {
            "code": 200,
            "token": None,
            "message": "Logout success"
        }
        return SimpleNamespace(**response)

    def authenticate(self, token, origin, ip_address):
        conn, cursor = self._connect_db()
        token_check_query = f"SELECT * FROM tokens WHERE token = {repr(token)} AND origin = {repr(origin)} AND ip_address = {repr(ip_address)} AND revoked_at IS NULL AND expiry > CURRENT_TIMESTAMP"
        cursor.execute(token_check_query)
        token = cursor.fetchone()
        self._disconnect_db(conn, cursor)
        if not token:
            return False
        return True
    
    def current_user(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user_id = payload['user_id']
            conn, cursor = self._connect_db()
            user_check_query = f"SELECT * FROM users WHERE id = {user_id} AND active = true"
            cursor.execute(user_check_query)
            user = cursor.fetchone()
            self._disconnect_db(conn, cursor)
            if not user:
                return None
            columns = [desc[0] for desc in cursor.description]
            user = dict(zip(columns, user))
            return SimpleNamespace(**user)
        except jwt.ExpiredSignatureError:
            return None
        
    def reset_password_token(self, email):
        conn, cursor = self._connect_db()
        user_check_query = f"SELECT * FROM users WHERE email = {repr(email)} AND active = true"
        cursor.execute(user_check_query)
        user = cursor.fetchone()
        self._disconnect_db(conn, cursor)
        if not user:
            return None
        return self._generate_reset_password_token(user[0])

    def reset_password(self, token, password):
        # hash password
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        # connect to database
        conn, cursor = self._connect_db()

        # check token
        token_check_query = f"SELECT * FROM users WHERE reset_password_token = {repr(token)} AND reset_password_sent_at > CURRENT_TIMESTAMP - INTERVAL '1 day' AND active = true"
        cursor.execute(token_check_query)
        user = cursor.fetchone()
        if not user:
            return False
        
        # reset password
        reset_password_query = f"UPDATE users SET encrypted_password = {repr(encrypted_password)}, reset_password_token = NULL, reset_password_sent_at = NULL, reset_password_at = CURRENT_TIMESTAMP WHERE id = {user[0]}"
        cursor.execute(reset_password_query)
        self._disconnect_db(conn, cursor)
        return True

    def _connect_db(self):
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        return [conn, cursor]
    
    def _disconnect_db(self, conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()
    
    def _check_existing_user(self, email):
        conn, cursor = self._connect_db()
        email_check_query = f"SELECT * FROM users WHERE email = {email} AND active = true"
        cursor.execute(email_check_query)
        existing_user = cursor.fetchone()
        self._disconnect_db(conn, cursor)
        return existing_user
    
    def _generate_token(self, user_id, origin, ip_address):
        conn, cursor = self._connect_db()
        expiry = datetime.datetime.now() + datetime.timedelta(days=1)
        payload = {
            "user_id": user_id,
            "origin": origin,
            "ip_address": ip_address,
            "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S.%f")
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        payload["token"] = token
        columns = ', '.join(payload.keys())
        values = '({})'.format(', '.join(map(repr, list(payload.values()))))
        insert_query = f"INSERT INTO tokens ({columns}) VALUES {values}"
        cursor.execute(insert_query)
        self._disconnect_db(conn, cursor)
        response = {
            "code": 200,
            "token": token,
            "message": "Success"
        }
        return SimpleNamespace(**response)
    
    def _response_user_already_exists(self):
        response = {
            "code": 409,
            "token": None,
            "message": "User already exists"
        }
        return SimpleNamespace(**response)
    
    def _response_invalid_credentials(self):
        response = {
            "code": 401,
            "token": None,
            "message": "Invalid credentials"
        }
        return SimpleNamespace(**response)

    def _generate_reset_password_token(self, user_id):
        conn, cursor = self._connect_db()
        expiry = datetime.datetime.now() + datetime.timedelta(days=1)
        payload = {
            "user_id": user_id,
            "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S.%f")
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        payload["token"] = token
        insert_query = f"UPDATE users SET reset_password_token = {repr(token)}, reset_password_sent_at = CURRENT_TIMESTAMP WHERE id = {user_id}"
        cursor.execute(insert_query)
        self._disconnect_db(conn, cursor)
        return token