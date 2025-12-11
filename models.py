from app import db

class Course(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)


class Lesson(db.Model):
    id = db.Column(db.String, primary_key=True)
    course_id = db.Column(db.String, db.ForeignKey('course.id'))
    title = db.Column(db.String, nullable=False)


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    course_id = db.Column(db.String, db.ForeignKey('course.id'))


class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    course_id = db.Column(db.String)
    lesson_id = db.Column(db.String)
    completed_at = db.Column(db.String)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    course_id = db.Column(db.String)
    score = db.Column(db.Integer)
    comment = db.Column(db.String)
    timestamp = db.Column(db.String)
