#  Human Security Management System

A secure web application implementing digital identity management using Keycloak for authentication and authorization.

[![Keycloak](https://img.shields.io/badge/Keycloak-23.0-blue)](https://www.keycloak.org/)
[![React](https://img.shields.io/badge/React-18.2-61dafb)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1)](https://www.mysql.com/)

---

## 👥 Team Members

- **Sarah Ibrahim**
- **Marina Kamil**
- **Rewan Khaled**
- **Sandra Hany**
- **Menna**
- **Shahed**

**Course**: Human Security — Final Project

---

## 📋 Table of Contents

- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Technologies Used](#️-technologies-used)
- [Prerequisites](#-prerequisites)
- [Installation Guide](#-installation-guide)
- [Database Schema](#️-database-schema)
- [User Roles & Permissions](#-user-roles--permissions)
- [API Endpoints](#-api-endpoints)
- [Test Users](#-test-users)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Troubleshooting](#️-troubleshooting)

---

## 🏗️ System Architecture

```
┌──────────────────┐
│   React Frontend │
│  (Port 3000)     │
└────────┬─────────┘
         │ JWT Token (Authorization Header)
         ▼
┌──────────────────┐
│    Keycloak      │
│   (Port 8080)    │
│  Authentication  │
│  & IAM Server    │
└────────┬─────────┘
         │ Token Validation (RS256)
         ▼
┌──────────────────┐
│  Flask Backend   │
│  (Port 5000)     │
│   API Server     │
│   + RBAC         │
└────────┬─────────┘
         │ SQL Queries
         ▼
┌──────────────────┐
│   MySQL DB       │
│  (Port 3306)     │
│   Data Storage   │
└──────────────────┘
```

**Flow**:
1. User accesses Frontend → Redirected to Keycloak Login
2. Keycloak authenticates user → Issues JWT Token
3. Frontend sends requests with JWT Token in Authorization header
4. Backend validates token signature, expiration, and roles
5. If authorized, Backend processes request and queries database
6. Response sent back to Frontend

---

##  Features

###  Security Features

- ✅ **OAuth 2.0 Authorization Code Flow** - Industry-standard secure authentication
- ✅ **JWT Token Validation** - Backend verifies token signature (RS256) and expiration
- ✅ **Role-Based Access Control (RBAC)** - Three-tier permission system
- ✅ **Zero Password Exposure** - Frontend never handles or stores passwords
- ✅ **Secure API Communication** - All requests authenticated with Bearer tokens
- ✅ **Token Auto-Refresh** - Automatic token renewal before expiration
- ✅ **Centralized Identity Management** - Single source of truth via Keycloak

### 📚 Functional Features

- ✅ **Student Management** - Full CRUD operations with role-based access
- ✅ **Staff Management** - Administrative controls for staff records
- ✅ **Admin Panel** - Complete system access and user management
- ✅ **Excel User Import** - Bulk user creation via Keycloak Admin REST API
- ✅ **Custom Login Theme** - University-branded Keycloak login page
- ✅ **Dynamic UI** - Interface adapts based on user roles
- ✅ **Real-time Validation** - Immediate feedback on operations

---

## Technologies Used

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Frontend** | React 18.2 | User interface framework |
| | Keycloak.js 23.0 | Authentication client |
| | Axios 1.6 | HTTP client for API calls |
| **Backend** | Flask 3.0+ | REST API server |
| | PyJWT 2.8+ | JWT token validation |
| | Flask-CORS | Cross-origin request handling |
| | mysql-connector-python | Database driver |
| **Database** | MySQL 8.0+ | Relational database |
| **IAM** | Keycloak 23.0+ | Identity & Access Management |
| **Protocol** | OAuth 2.0 | Authorization framework |

---

## Prerequisites

Before starting, ensure you have installed:

- ✅ **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- ✅ **Node.js 16+** - [Download here](https://nodejs.org/)
- ✅ **MySQL 8.0+** - [Download here](https://dev.mysql.com/downloads/)
- ✅ **Keycloak 23+** - [Download here](https://www.keycloak.org/downloads)
- ✅ **Git** - [Download here](https://git-scm.com/downloads)

**Recommended Tools**:
- VS Code with Live Server extension
- MySQL Workbench
- Postman (for API testing)

---

## 📦 Installation Guide

### Step 1: Clone Repository

```bash
git clone https://github.com/other3li/Human-Security-Final-Project.git
cd Human-Security-Final-Project
```

---

### Step 2: MySQL Database Setup

```bash
mysql -u root -p

# Create database
CREATE DATABASE university_db;

EXIT;
```

> **Note**: Tables will be created automatically when backend starts

---

### Step 3: Keycloak Configuration

#### 3.1 Start Keycloak

```bash
cd keycloak/bin

# Windows:
kc.bat start-dev
```

Wait until you see: `Listening on: http://0.0.0.0:8080`

#### 3.2 Access Admin Console

- **URL**: http://localhost:8080/admin
- **Username**: `admin`
- **Password**: `admin`

#### 3.3 Create Realm

1. Click **"Create Realm"**
2. **Realm name**: `university-realm`
3. Click **"Create"**

#### 3.4 Create Roles

1. Navigate to **"Realm roles"**
2. Click **"Create role"** and add:
   - `student`
   - `staff`
   - `admin`

#### 3.5 Create Frontend Client

1. Go to **"Clients"** → **"Create client"**
2. **General Settings**:
   - Client ID: `frontend-client`
   - Client authentication: `OFF`
   - Click **"Next"**
3. **Capability config**:
   - Standard flow: `ON`
   - Direct access grants: `ON`
   - Click **"Next"**
4. **Login settings**:
   - Root URL: `http://localhost:3000`
   - Valid redirect URIs: `http://localhost:3000/*`
   - Valid post logout redirect URIs: `http://localhost:3000/*`
   - Web origins: `http://localhost:3000`
   - Click **"Save"**

#### 3.6 Create Backend Client

1. Create another client
2. **General Settings**:
   - Client ID: `backend-client`
   - Client authentication: `ON`
   - Click **"Next"**
3. **Capability config**:
   - Service accounts roles: `ON`
   - Click **"Next"** then **"Save"**

---

### Step 4: Backend Setup

```bash
cd backend

python -m venv venv
venv\Scripts\activate
pip install flask flask-cors flask-jwt-extended mysql-connector-python openpyxl requests
pip install -r requirements.txt
```

#### 4.1 Configure JWT Public Key

1. Go to: http://localhost:8080/admin
2. Select **university-realm** → **Realm Settings** → **Keys**
3. Find **RS256** algorithm
4. Click **"Public key"** button and copy the key
5. Open `backend/app.py`
6. Replace `JWT_PUBLIC_KEY` value with the copied key (add `-----BEGIN PUBLIC KEY-----` and `-----END PUBLIC KEY-----` wrapper if needed)

#### 4.2 Run Backend

```bash
python app.py
```

Expected output:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

---

### Step 5: Import Users from Excel

```bash
python create_users.py
```

**Expected Output**:
```
============================================================
🚀 Starting User Import from Excel to Keycloak
============================================================
🔑 Getting admin token...
📄 Reading Excel file: users.xlsx
👥 Processing users...

[Row 2] Processing: ahmed.student
✅ Created user: ahmed.student with role: student
[Row 3] Processing: sara.staff
✅ Created user: sara.staff with role: staff
[Row 4] Processing: admin.user
✅ Created user: admin.user with role: admin
...
============================================================
✅ Import Complete!
   Successfully created: 6 users
   Failed: 0 users
============================================================
```

![User Import Success](https://github.com/user-attachments/assets/747ccb2f-4905-415d-a2de-e2b21be2b358)

---

### Step 6: Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will automatically open at: **http://localhost:3000**

---

### Step 7: Apply Custom Login Theme (Optional)

```bash
# Copy theme to Keycloak themes folder
cp -r keycloak/themes/university-theme /path/to/keycloak/themes/
```

**Then in Keycloak Admin Console**:
1. **Realm Settings** → **Themes**
2. **Login theme**: Select `university-theme`
3. Click **"Save"**
4. Logout and login again to see the custom theme

---

## Database Schema

### Students Table
```sql
CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Staff Table
```sql
CREATE TABLE staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    position VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Admin Table
```sql
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎭 User Roles & Permissions

| Role | Permissions | Allowed Operations |
|------|-------------|-------------------|
|  **Student** | Read Only | • View students list<br>• View own profile |
|  **Staff** | Create, Read, Update | • All Student permissions<br>• Add new students<br>• Edit student records<br>• View staff list |
| **Admin** | Full CRUD | • All Staff permissions<br>• Delete records<br>• Manage staff<br>• Full system access |

### Role Enforcement Layers:

1. **Frontend**: UI elements hidden/shown based on user roles
2. **Backend**: API endpoints protected with `@role_required` decorator
3. **Keycloak**: Central role management and assignment

---

## 🔌 API Endpoints

### Students API

| Method | Endpoint | Required Roles | Description |
|--------|----------|---------------|-------------|
| `GET` | `/students` | student, staff, admin | Retrieve all students |
| `POST` | `/students` | staff, admin | Create new student |
| `PUT` | `/students/<id>` | staff, admin | Update student by ID |
| `DELETE` | `/students/<id>` | admin | Delete student by ID |

**Example Request**:
```bash
curl -X GET http://localhost:5000/students \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Staff API

| Method | Endpoint | Required Roles | Description |
|--------|----------|---------------|-------------|
| `GET` | `/staff` | staff, admin | Retrieve all staff |
| `POST` | `/staff` | admin | Create new staff member |
| `PUT` | `/staff/<id>` | admin | Update staff by ID |
| `DELETE` | `/staff/<id>` | admin | Delete staff by ID |

### Admin API

| Method | Endpoint | Required Roles | Description |
|--------|----------|---------------|-------------|
| `GET` | `/admins` | admin | Retrieve all admins |
| `POST` | `/admins` | admin | Create new admin |
| `PUT` | `/admins/<id>` | admin | Update admin by ID |
| `DELETE` | `/admins/<id>` | admin | Delete admin by ID |

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - User lacks required role/permission
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Test Users

| Username | Password | Role | Access Level |
|----------|----------|------|--------------|
| `ahmed.student` | Pass123 | Student | Read only |
| `sara.staff` | Pass123 | Staff | Create, Read, Update |
| `admin.user` | Pass123 | Admin | Full CRUD |
| `mohamed.student` | Pass123 | Student | Read only |
| `fatima.staff` | Pass123 | Staff | Create, Read, Update |
| `omar.admin` | Pass123 | Admin | Full CRUD |

---

##  Screenshots

### 1. Custom Keycloak Login Page
*University-branded login interface with custom styling*

### 2. User Dashboard
*Main application dashboard showing user information and role-based actions*

### 3. Students Management
*Students list with CRUD operations based on user roles*

### 4. Staff Management
*Staff records with admin-only access controls*

### 5. Keycloak Admin Console
*Realm configuration showing roles, clients, and users*

### 6. Excel User Import Success
*Successful bulk user import via Keycloak Admin API*

---

##  Project Structure

```
Human-Security-Final-Project/
│
├── frontend/                   # React Frontend Application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js             # Main component with auth logic
│   │   ├── App.css            # Application styling
│   │   ├── keycloak.js        # Keycloak client configuration
│   │   └── index.js           # React entry point
│   ├── package.json           # Node dependencies
│   └── README.md
│
├── backend/                    # Flask API Server
│   ├── app.py                 # Main Flask application
│   ├── create_users.py        # Excel user import script
│   ├── requirements.txt       # Python dependencies
│   └── README.md
│
├── keycloak/                   # Keycloak Configuration
│   └── themes/
│       └── university-theme/  # Custom login theme
│           ├── login/
│           │   ├── theme.properties
│           │   ├── login.ftl  # Login page template
│           │   └── resources/
│           │       └── css/
│           │           └── university.css
│
├── excel/
│   └── users.xlsx             # User data for bulk import
│
├── database/
│   └── schema.sql             # Database schema documentation
│
├── screenshots/               # Application screenshots
│   ├── login.png
│   ├── dashboard.png
│   ├── students.png
│   ├── staff.png
│   └── keycloak-config.png
│
└── README.md                  # This file
```

---

## Troubleshooting

### Issue 1: "Client not found" Error

**Symptom**: Error message on frontend: "We are sorry... Client not found"

**Solution**:
1. Verify `frontend-client` exists in Keycloak
2. Check client name matches in `frontend/src/keycloak.js`
3. Ensure client is enabled and properly configured

### Issue 2: "Unauthorized" (401) Error

**Symptom**: API requests failing with 401 status

**Solution**:
1. Verify JWT public key in `backend/app.py` matches Keycloak realm key
2. Check token hasn't expired
3. Ensure token is being sent in Authorization header

### Issue 3: CORS Error

**Symptom**: Cross-origin request blocked in browser console

**Solution**:
1. Verify Flask-CORS is installed: `pip install flask-cors`
2. Check CORS configuration in `app.py`:
   ```python
   CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
   ```

### Issue 4: Keycloak Won't Start

**Symptom**: Port 8080 already in use

**Solution**:
```bash
# Windows: Check what's using port 8080
netstat -ano | findstr :8080

# Kill the process using the PID from above
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8080 | xargs kill -9
```

### Issue 5: Database Connection Failed

**Symptom**: Backend can't connect to MySQL

**Solution**:
1. Verify MySQL is running
2. Check credentials in `app.py`:
   ```python
   db = mysql.connector.connect(
       host="localhost",
       user="root",
       password="",  # Your MySQL password
       database="university_db"
   )
   ```
3. Ensure `university_db` database exists

### Issue 6: Users Not Importing from Excel

**Symptom**: Script fails or creates users without roles

**Solution**:
1. Check Excel file format matches expected structure
2. Verify roles exist in Keycloak before import
3. Ensure Keycloak admin credentials are correct in script

---

## Running the Complete System

**Open 4 terminals**:

```bash
# Terminal 1: Start Keycloak
cd keycloak/bin
kc.bat start-dev

# Terminal 2: Start Backend
cd backend
python app.py

# Terminal 3: Start Frontend
cd frontend
npm start

# Terminal 4: Import Users (run once)
cd backend
python create_users.py
```

**Access URLs**:
- 🌐 Frontend Application: http://localhost:3000
- 🔌 Backend API: http://localhost:5000
- 🔐 Keycloak Server: http://localhost:8080
- ⚙️ Keycloak Admin: http://localhost:8080/admin

---


- **GitHub Repository**: [Human-Security-Final-Project](https://github.com/other3li/Human-Security-Final-Project)
- **Issues**: [Report an Issue](https://github.com/other3li/Human-Security-Final-Project/issues)
