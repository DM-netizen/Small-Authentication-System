# Flask Authentication System

This is a simple authentication system built using Flask and Bootstrap. It includes user login, logout, a dashboard, and a home page.

## Features
- User authentication (login/logout)
- Dashboard page (accessible only to logged-in users)
- Home page (accessible to all)
- Session-based authentication management
- Frontend styled with Bootstrap

## Technologies Used
- Flask (Python web framework)
- Flask-Login (User session management)
- Flask-WTF (Forms handling)
- SQLite (Database)
- Bootstrap (Frontend styling)

## Installation

### Prerequisites
Ensure you have Python installed (preferably Python 3.8 or later).

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/flask-auth-system.git
   cd flask-auth-system
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
5. Run the application:
   ```sh
   flask run
   ```
6. Open your browser and go to `http://127.0.0.1:5000/`

## Project Structure
```
flask-auth-system/
│-- app/
│   │-- static/ (CSS, JS, images)
│   │-- templates/ (HTML templates)
│   │-- routes.py (Defines application routes)
│   │-- models.py (Database models)
│   │-- forms.py (Flask-WTF forms)
│   └-- __init__.py (App initialization)
│-- migrations/ (Database migrations)
│-- requirements.txt (Python dependencies)
│-- config.py (Configuration settings)
│-- run.py (Entry point to run the app)
└-- README.md (Project documentation)
```

## Usage
- Visit the home page (`/`)
- Register (if registration is enabled)
- Login using your credentials (`/login`)
- Access the dashboard (`/dashboard`)
- Logout (`/logout`)


## License
This project is licensed under the MIT License.
