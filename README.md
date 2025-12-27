# Human-Security-Management-System

A secure web application implementing digital identity management using Keycloak for authentication and authorization.

 Table of Contents

System Architecture
Features
Technologies Used
Prerequisites
Installation
Database Schema
User Roles
API Endpoints
Test Users
Screenshots
Project Structure


Prerequisites 
Keycloak running locally
Recommended: VS Code + Live Server extension
MySQL 
python 

# System Architecture
┌──────────────────┐
│   React Frontend │
│  (Port 3000)     │
└────────┬─────────┘
         │ JWT Token
         ▼
┌──────────────────┐
│    Keycloak      │
│   (Port 8080)    │
│  Authentication  │
└────────┬─────────┘
         │ Token Validation
         ▼
┌──────────────────┐
│  Flask Backend   │
│  (Port 5000)     │
│   API Server     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   MySQL DB       │
│  (Port 3306)     │
│   Data Storage   │
└──────────────────┘

Features
 Security Features

✅ OAuth 2.0 Authorization Code Flow - Secure authentication
✅ JWT Token Validation - Backend verifies token signature and expiration
✅ Role-Based Access Control (RBAC) - Three-tier permission system
✅ No Password Storage in Frontend - All authentication via Keycloak
✅ Secure API Communication - All requests use Bearer tokens

 Functional Features

✅ Student Management - Full CRUD operations
✅ Staff Management - Administrative controls
✅ Admin Panel - Complete system access
✅ Excel User Import - Bulk user creation via Admin API
✅ Custom Login Theme - University-branded Keycloak login page

📁 Project Structure
Human-Security-Final-Project/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Styling
│   │   ├── keycloak.js         # Keycloak configuration
│   │   └── index.js            # Entry point
│   ├── package.json
│   └── README.md
│
├── backend/
│   ├── app.py                  # Flask API server
│   ├── create_users.py         # Excel user import script
│   ├── requirements.txt        # Python dependencies
│   └── README.md
│
├── keycloak/
│   └── themes/
│       └── university-theme/   # Custom login theme
│           ├── login/
│           │   ├── theme.properties
│           │   ├── login.ftl
│           │   └── resources/
│           │       └── css/
│           │           └── university.css
│
├── excel/
│   └── users.xlsx              # User import data
│
├── database/
│   └── schema.sql              # Database schema
│
├── screenshots/
│   ├── login.png
│   ├── dashboard.png
│
└── README.md                   # This file


Installation 
MySQL Database Setup
CREATE DATABASE university_db; 

 Keycloak Setup
Start Keycloak:
bashcd keycloak/bin
./kc.bat start-dev
# or on Linux/Mac: ./kc.sh start-dev
Access Admin Console:

URL: http://localhost:8080/admin
Username: admin
Password: admin

Configure Realm:
Create Realm:

Click "Create Realm"
Realm name: university-realm
Click "Create"

Create Roles:

Go to "Realm roles"
Create three roles:

student
staff
admin



Create Frontend Client:

Go to "Clients" → "Create client"
Client ID: frontend-client
Client authentication: OFF
Standard flow: ON
Valid redirect URIs: http://localhost:3000/*
Web origins: http://localhost:3000
Click "Save"

Create Backend Client:

Create another client
Client ID: backend-client
Client authentication: ON
Service accounts roles: ON
Click "Save"

Backend Setup 
cd backend
python -m venv venv
venv\Scripts\activate
pip install flask flask-cors flask-jwt-extended mysql-connector-python openpyxl requests
pip install -r requirements.txt

# Get Keycloak Public Key
# Go to: http://localhost:8080/admin → university-realm → Realm Settings → Keys
# Copy the RS256 Public Key and paste it in app.py JWT_PUBLIC_KEY

 Run backend
python app.py


Import Users from Excel 
python create_users.py
![WhatsApp Image 2025-12-26 at 1 30 43 PM](https://github.com/user-attachments/assets/747ccb2f-4905-415d-a2de-e2b21be2b358)

Frontend Setup 
cd frontend
npm install
npm start
Frontend will open automatically at: http://localhost:3000

Apply Custom Login Them
cp -r keycloak/themes/university-theme /path/to/keycloak/themes/


Troubleshooting 
Issue: "Client not found"
Solution: Create frontend-client in Keycloak with correct settings
Issue: "Unauthorized" errors
Solution: Check JWT public key in app.py matches Keycloak realm key
Issue: "CORS error"
Solution: Ensure Flask-CORS is installed and configured for http://localhost:3000
Issue: Keycloak won't start
Solution: Check if port 8080 is already in use: netstat -ano | findstr :8080



Authors 
Sarah Ibrahim /Marina Kamil /rewan Khaled / Sandra Hany / menna / Shahed 
Human Security — Final Project
