# Online Learning Platform API (Flask + SQLAlchemy)

Features:
- Course Enrollment
- Lesson Completion (Idempotent)
- Progress Tracking
- Rating System (One per user)
- Lesson Access Control

Run:
```
pip install flask flask_sqlalchemy
python app.py
```
Send X-User-Id header for user identity.



This project is a simple Flask-based API that lets users enroll in courses, complete 

lessons, track progress, and submit ratings.

Features

 1.Enroll a user into a course

2.Get all lessons in a course

3.Mark a lesson as completed

4.Track user’s progress

5.Rate a course

Tech Stack :

Python

Flask

JSON (file-based storage)

REST API

Endpoints
1. Enroll in a Course

POST /courses/<course_id>/enroll

2. Get Lessons

GET /courses/<course_id>/lessons

3. Complete a Lesson

POST /courses/<course_id>/lessons/<lesson_id>/complete

4. Track Progress

GET /users/<user_id>/courses/<course_id>/progress

5. Rate a Course

POST /courses/<course_id>/rating

How to Run
pip install flask
python app.py


Server runs at:
http://127.0.0.1:5000
