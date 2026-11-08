# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Teacher login and student registration management

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Create a teacher account. The password is stored as a salted PBKDF2 hash in the local, Git-ignored `src/teachers.json`, not as plaintext:

   ```
   python -m src.manage_teachers
   ```

   The command creates the local credentials file from `src/teachers.example.json` if needed. Run it again to add a teacher or update an existing teacher's password. Keep the local credentials file private.

3. Run the application from the repository root:

   ```
   uvicorn src.app:app --reload
   ```

   Set `COOKIE_SECURE=true` when serving the application over HTTPS.

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Publicly view activities and participants                           |
| POST   | `/auth/login`                                                      | Log in with a teacher username and password                          |
| GET    | `/auth/me`                                                         | Get the current teacher session                                      |
| POST   | `/auth/logout`                                                     | Log out                                                              |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Register a student (teacher login required)                          |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher login required)                     |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

Activity registrations and teacher sessions are stored in memory, so they reset when the server restarts. Teacher password hashes are stored in `src/teachers.json`.
