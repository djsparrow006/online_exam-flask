from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models import Question, Result

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
def dashboard():
    if "role" not in session or session["role"] != "admin":
        flash("Admins only!", "danger")
        return redirect(url_for("home"))
    questions = Question.query.all()
    results = Result.query.all()
    return render_template("admin.html", questions=questions, results=results)

@admin_bp.route("/add_question", methods=["POST"])
def add_question():
    if "role" not in session or session["role"] != "admin":
        flash("Admins only!", "danger")
        return redirect(url_for("home"))

    q = Question(
        question=request.form["question"],
        option_a=request.form["option_a"],
        option_b=request.form["option_b"],
        option_c=request.form["option_c"],
        option_d=request.form["option_d"],
        answer=request.form["answer"]
    )
    db.session.add(q)
    db.session.commit()
    flash("Question added successfully!", "success")
    return redirect(url_for("admin.dashboard"))
