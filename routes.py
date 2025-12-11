
from flask import request, jsonify
from datetime import datetime
from functools import wraps
from app import app, db
from models import Course, Lesson, Enrollment, Completion, Rating

def get_user_id():
    return request.headers.get("X-User-Id")


def require_user(func):
    @wraps(func)
    def wrapper(*a, **kw):
        uid = get_user_id()
        if not uid:
            return jsonify({"error": "user id required"}), 401
        return func(uid, *a, **kw)
    return wrapper


@app.route("/courses/<cid>/enroll", methods=["POST"])
@require_user
def enroll(uid, cid):
    if not Course.query.get(cid):
        return jsonify({"error": "course not found"}), 404

    if Enrollment.query.filter_by(user_id=uid, course_id=cid).first():
        return jsonify({"message": "already enrolled"}), 409

    db.session.add(Enrollment(user_id=uid, course_id=cid))
    db.session.commit()

    return jsonify({"message": "enrolled successfully"}), 201




@app.route("/courses/<cid>/lessons/<lid>/complete", methods=["POST"])
@require_user
def complete(uid, cid, lid):
    if not Lesson.query.filter_by(id=lid, course_id=cid).first():
        return jsonify({"error": "lesson not found"}), 404
    if not Enrollment.query.filter_by(user_id=uid, course_id=cid).first():
        return jsonify({"error": "not enrolled"}), 403

    exists = Completion.query.filter_by(user_id=uid, course_id=cid, lesson_id=lid).first()
    if exists:
        return jsonify({"message": "already completed", "completedAt": exists.completed_at}), 200

    ts = datetime.utcnow().isoformat() + "Z"
    db.session.add(Completion(user_id=uid, course_id=cid, lesson_id=lid, completed_at=ts))
    db.session.commit()

    return jsonify({"message": "completed", "completedAt": ts}), 201


@app.route("/users/<uid>/courses/<cid>/progress")
def progress(uid, cid):
    lessons = Lesson.query.filter_by(course_id=cid).all()
    total = len(lessons)
    completed = Completion.query.filter_by(user_id=uid, course_id=cid).count()
    percent = (completed / total * 100) if total else 0

    return jsonify({
        "courseId": cid,
        "userId": uid,
        "completedLessons": completed,
        "totalLessons": total,
        "percentage": round(percent, 2)
    })




@app.route("/courses/<cid>/rating", methods=["POST"])
@require_user
def rate(uid, cid):
    # Must be enrolled
    if not Enrollment.query.filter_by(user_id=uid, course_id=cid).first():
        return jsonify({"error": "must enroll to rate"}), 403

    data = request.json or {}
    score = data.get("score")
    comment = data.get("comment")

    if score is None or not (1 <= int(score) <= 5):
        return jsonify({"error": "score must be 1–5"}), 400

    # Check existing rating
    existing = Rating.query.filter_by(user_id=uid, course_id=cid).first()

    if existing:
        existing.score = int(score)
        existing.comment = comment
        existing.timestamp = datetime.utcnow().isoformat() + "Z"
    else:
        new_rating = Rating(
            user_id=uid,
            course_id=cid,
            score=int(score),
            comment=comment,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        db.session.add(new_rating)

    db.session.commit()

    return jsonify({"message": "rating submitted"}), 201







def rating(cid):
    r = Rating.query.filter_by(course_id=cid).all()
    if not r:
        return jsonify({"average": 0, "count": 0})

    scores = [x.score for x in r]
    avg = sum(scores) / len(scores)

    return jsonify({"average": round(avg, 2), "count": len(scores)})


@app.route("/courses/<cid>/lessons")
@require_user
def lessons(uid, cid):
    if not Enrollment.query.filter_by(user_id=uid, course_id=cid).first():
        return jsonify({"error": "forbidden"}), 403

    ls = Lesson.query.filter_by(course_id=cid).all()
    return jsonify({"lessons": [{"id": l.id, "title": l.title} for l in ls]})


@app.route("/")
def home():
    return jsonify({"message": "Learning Platform API is running"})
