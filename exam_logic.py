from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models import Question, Result

exam_bp = Blueprint("exam", __name__)

@exam_bp.route("/start", methods=["GET", "POST"])
def start_exam():
    if "user_id" not in session or session.get("role") != "student":
        flash("Please login as student.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        score = 0
        questions = Question.query.all()

        for q in questions:
            user_answer = request.form.get(str(q.id))
            if user_answer and user_answer == q.answer:
                score += 1

        result = Result(user_id=session["user_id"], score=score)
        db.session.add(result)
        db.session.commit()

        flash(f"Exam finished! You scored {score}/{len(questions)}.", "success")
        return redirect(url_for("exam.results"))

    questions = Question.query.all()
    return render_template("exam.html", questions=questions)

@exam_bp.route("/results")
def results():
    if "user_id" not in session:
        flash("Please login first.", "danger")
        return redirect(url_for("home"))

    results = Result.query.filter_by(user_id=session["user_id"]).all()
    return render_template("results.html", results=results)
