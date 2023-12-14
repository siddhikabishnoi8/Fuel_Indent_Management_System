# Fuel Indent Management System (FIMS)

## Introduction
The Fuel Indent Management System (FIMS) is a web-based application designed to streamline the fuel indenting processes within organizational setups. The application serves as a digital platform to manage fuel orders, facilitating efficiency and transparency in operations.

## Features
- Real-time tracking of fuel orders
- Automated notifications
- User-friendly interface for administrators and end-users
- Centralized control over user management and supplier coordination
- Real-time insights into fuel indent statuses

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **PDF Generation**: ReportLab
- **User Authentication**: Flask-Login

## Setup and Installation

### Prerequisites
- Python 3.x
- MySQL server
- pip (Python package manager)

### Steps to Run the Application
1. **Clone the Repository**:
   ```bash
   git clone [repository-url]
   cd [repository-name]
    ```

2. **Set Up a Virtual Environment (Optional but recommended)**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Required Packages**:

```bash
pip install -r requirements.txt
```

4. **Configure Database**:

- Ensure MySQL server is running.
- Create a database named fuel_db.
- Modify the SQLALCHEMY_DATABASE_URI in app.py to reflect your MySQL user and password.

5. **Initialize the Database**:

```bash
python3
>>> from app import db
>>> db.create_all()
```

6. **Run the Application**:

```bash
python app.py
```
7. **The application will be accessible at http://localhost:5000**.

## Usage
- Visit http://localhost:5000 on your browser.
- Register as a new user or login.
- Navigate through the application to manage fuel indents, suppliers, and user accounts.

## Contribution

Feel free to fork this repository and contribute. Please follow the existing code style and use meaningful commit messages.
