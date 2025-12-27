from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
import mysql.connector
import requests
from functools import wraps
import jwt as pyjwt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# ---------------- Keycloak Config ----------------
KEYCLOAK_URL = "http://localhost:8080"
REALM = "university-realm"
CLIENT_ID = "university-backend"

# ---------------- JWT Config ----------------
app.config["JWT_ALGORITHM"] = "RS256"
app.config["JWT_PUBLIC_KEY"] = """eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuMWNJM3pvZzRJOWFkc0NFTHU0M2lWSkdfU2t6dUd2Z3cxQzJycWNQWVlNIn0.eyJleHAiOjE3NjY3ODM2MzYsImlhdCI6MTc2Njc4MzMzNiwianRpIjoib25ydHJvOjgwMGMyZjI3LTQ4MDUtOTZkYy03MjdmLTE2ZTllMGNmYWYyNCIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC9yZWFsbXMvdW5pdmVyc2l0eS1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJiMjcwYTc0YS0wNzEzLTRkOGUtYjcyNC1hN2Q3ZTYyZjk3MmQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmcm9udGVuZC1jbGllbnQiLCJzaWQiOiI4MWM1N2ZjMy1lMWEyLTY0OTEtNmRhNy02MjU1NTEwMzkxM2MiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic3R1ZGVudCIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXVuaXZlcnNpdHktcmVhbG0iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJhbGkgbW9oYW1kIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWxpIiwiZ2l2ZW5fbmFtZSI6ImFsaSIsImZhbWlseV9uYW1lIjoibW9oYW1kIiwiZW1haWwiOiJzYXJha2FkYXMyMzQ1NkBnbWFpbC5jb20ifQ.X2_6cw5okN_G6BcjkJ2pjjB_zTjIvqnz4RWrbLjWoQQI2Of5r2wEroMLmskJ0ZkA3d8TDmkCXuvlVLnLeVWEBqjBKb27T5n3iPAnFoDow0WuInNVK9v6-uDNTWhH7ju7YwH8Rk18dv0Ot_WIyZ-VMEJl6JTXDN26ZSxQfSMbLZjU10Hj2OeBwFkU9Pqf7pNceyTPvoaEdmw3aGCE0WlxCLA1irdYVBrsUvCkdHCs6LE9p19irL6bO-h4oVMZKsfX3d0nWMsSRg6eyqrbj3vjDBRUHBcI0aKaGWwW-UEgEo8I_fu13Vsx51LFwqLfr1cVnA0htr-Pzrc-pM8xCc0xNw"""

jwt_manager = JWTManager(app)

# ---------------- Custom JWT Verification ----------------
def verify_token():
    """Manual JWT verification from Authorization header"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    
    try:
        # Decode and verify JWT
        decoded = pyjwt.decode(
            token,
            app.config["JWT_PUBLIC_KEY"],
            algorithms=[app.config["JWT_ALGORITHM"]],
            audience=CLIENT_ID,
            options={"verify_exp": True}
        )
        return decoded
    except pyjwt.ExpiredSignatureError:
        return None
    except pyjwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        decoded = verify_token()
        if not decoded:
            return jsonify({"msg": "Unauthorized: Invalid or expired token"}), 401
        
        # Attach decoded token to request context
        request.decoded_token = decoded
        return f(*args, **kwargs)
    return decorated

def role_required(allowed_roles):
    """Decorator to check if user has required role"""
    def wrapper(fn):
        @token_required
        def decorator(*args, **kwargs):
            decoded = request.decoded_token
            user_roles = decoded.get("realm_access", {}).get("roles", [])
            
            if not any(role in user_roles for role in allowed_roles):
                return jsonify({"msg": "Forbidden: insufficient role"}), 403
            
            return fn(*args, **kwargs)
        decorator.__name__ = fn.__name__
        return decorator
    return wrapper

# ---------------- Database Connection ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="university_db"
)
cursor = db.cursor(dictionary=True)

# Create tables (same as before)
cursor.execute("CREATE DATABASE IF NOT EXISTS university_db")
cursor.execute("USE university_db")

cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    position VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"msg": "Backend is running!"}), 200

@app.route("/protected", methods=["GET"])
@token_required
def protected():
    return jsonify({
        "msg": "You accessed a protected route!",
        "user": request.decoded_token.get("preferred_username"),
        "roles": request.decoded_token.get("realm_access", {}).get("roles", [])
    }), 200

# ---------------- Student CRUD ----------------
@app.route("/students", methods=["GET"])
@role_required(["student", "staff", "admin"])
def get_students():
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    return jsonify(students), 200

@app.route("/students", methods=["POST"])
@role_required(["staff", "admin"])
def add_student():
    data = request.json
    cursor.execute(
        "INSERT INTO student (first_name, last_name, email) VALUES (%s,%s,%s)",
        (data["first_name"], data["last_name"], data["email"])
    )
    db.commit()
    return jsonify({"msg": "Student added"}), 201

@app.route("/students/<int:id>", methods=["PUT"])
@role_required(["staff", "admin"])
def update_student(id):
    data = request.json
    cursor.execute(
        "UPDATE student SET first_name=%s, last_name=%s, email=%s WHERE student_id=%s",
        (data["first_name"], data["last_name"], data["email"], id)
    )
    db.commit()
    return jsonify({"msg": "Student updated"}), 200

@app.route("/students/<int:id>", methods=["DELETE"])
@role_required(["admin"])
def delete_student(id):
    cursor.execute("DELETE FROM student WHERE student_id=%s", (id,))
    db.commit()
    return jsonify({"msg": "Student deleted"}), 200

# ---------------- Staff CRUD (same pattern) ----------------
@app.route("/staff", methods=["GET"])
@role_required(["staff", "admin"])
def get_staff():
    cursor.execute("SELECT * FROM staff")
    staff = cursor.fetchall()
    return jsonify(staff), 200

@app.route("/staff", methods=["POST"])
@role_required(["admin"])
def add_staff():
    data = request.json
    cursor.execute(
        "INSERT INTO staff (first_name, last_name, email, position) VALUES (%s,%s,%s,%s)",
        (data["first_name"], data["last_name"], data["email"], data["position"])
    )
    db.commit()
    return jsonify({"msg": "Staff added"}), 201


if __name__ == "__main__":
    app.run(port=5000, debug=True)