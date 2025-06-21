# 📝 Feedback Tool

An internal feedback sharing tool for managers and employees. It supports structured feedback, sentiment tracking, feedback history, employee acknowledgments, and email notifications.

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/feedback-tool.git
cd feedback-tool
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL
Create a database:
```sql
CREATE DATABASE feedback_db;
```

### 4. Environment Configuration

Set environment variables in `.env` or directly in `config.py`:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/feedback_db
SECRET_KEY=your_secret_key
```

### 5. Run the App
```bash
python3 app.py
```

---

## 📦 Folder Structure
```
feedback_tool/
├── app.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── routes/
│   ├── feedback.py
│   └── user.py
├── migrations/
│   └── 001_create_tables.sql
└── requirements.txt
```

---

## 🔑 Authentication API

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "123456",
  "role": "manager"
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "123456"
}
```
Returns: `{ "access_token": "<jwt_token>" }`

---

## 📤 Feedback API

🔐 Include header:
```
Authorization: Bearer <jwt_token>
```

### Create Feedback (Manager Only)
```http
POST /feedback/
Content-Type: application/json

{
  "employee_id": 2,
  "strengths": "Great leadership",
  "improvements": "Improve focus",
  "sentiment": "positive",
  "tags": ["leadership", "communication"],
  "anonymous": false
}
```

### Update Feedback (Manager Only)
```http
PUT /feedback/<feedback_id>
Content-Type: application/json

{
  "improvements": "Time management"
}
```

### Acknowledge Feedback (Employee Only)
```http
PUT /feedback/<feedback_id>/acknowledge
```

### Comment on Feedback (Employee Only)
```http
PUT /feedback/<feedback_id>/comment
Content-Type: application/json

{
  "employee_comments": "Thanks for the feedback!"
}
```

---

## 👤 User API

### Get My Profile
```http
GET /user/me
```

### View Feedback Received (Employee)
```http
GET /user/feedback
```

---

## 📊 Manager Analytics API

### Team Overview
```http
GET /feedback/team-overview
```

Response:
```json
{
  "employees_count": 4,
  "total_feedbacks": 12,
  "sentiment_breakdown": {
    "positive": 7,
    "neutral": 3,
    "negative": 2
  }
}
```

---

## 📧 Email Notifications

When feedback is created, an email is automatically sent to the employee's registered email using `yagmail` and Gmail's SMTP.

Make sure to:
- Enable 2FA on Gmail
- Use an App Password for `APP_PASSWORD`

---
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# 🧱 Tech Stack & Design Decisions

This document explains the technologies used in this project and the reasoning behind the architectural and design choices.

---

## 🔧 Tech Stack

### Backend
- **Flask**: Lightweight and fast for building RESTful APIs.
- **Flask-JWT-Extended**: For secure authentication using JSON Web Tokens.
- **SQLAlchemy**: ORM for interacting with PostgreSQL in a Pythonic way.
- **Marshmallow**: For serialization/deserialization and validation of request/response schemas.
- **Yagmail**: Simplifies sending emails via Gmail with HTML support.

### Database
- **PostgreSQL**: Chosen for its reliability, support for JSON, enums, arrays, and advanced querying.
- **Alembic**: For database migrations and versioning.

---

## 🏗️ Key Design Decisions

### 🔐 Authentication & Roles
- JWT is used for stateless, secure authentication.
- `User` model has a `role` (`manager` or `employee`) to control access to endpoints.
- Access control is enforced at the route level using role checks after JWT validation.

### 🧾 Feedback Structure
- `Feedback` is a first-class entity linked to both manager and employee.
- Fields include `strengths`, `improvements`, `sentiment`, `tags`, `acknowledged`, and `anonymous`.
- `employee_comments` allows feedback loop and engagement from employees.

### 📬 Email Notification
- When feedback is created, a styled HTML email is sent to the employee via Gmail using Yagmail.
- Configuration uses environment variables: `SENDER_EMAIL`, `APP_PASSWORD`.

### 📊 Analytics (Team Overview)
- Endpoint `/feedback/team-overview` provides quick manager insights:
  - Count of employees who received feedback
  - Total feedbacks given
  - Sentiment breakdown (positive, neutral, negative)

### 📁 Project Structure
- Code is modular and organized by responsibility:
  - `auth.py`: Authentication logic
  - `routes/`: Separated `user.py` and `feedback.py`
  - `schemas.py`: Marshmallow validation
  - `models.py`: SQLAlchemy data models
  - `config.py`: Centralized configuration
  - `database.py`: Database instance