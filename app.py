# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, db
from models import User, Question, Result

app = Flask(__name__)
app.secret_key = "supersecretkey"  # for session & flash messages

# Initialize database
init_db(app)

# ----------------- LOGIN ROUTE -----------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            flash(f"Welcome, {user.username}!", "success")
            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("start_exam"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("home"))

    return render_template("login.html")

# ----------------- REGISTER ROUTE -----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm", "").strip()

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for("register"))
        if len(username) < 3 or len(password) < 6:
            flash("Username must be ≥3 chars and password ≥6 chars.", "danger")
            return redirect(url_for("register"))
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Username already taken.", "danger")
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)
        new_user = User(username=username, password=hashed, role="student")
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("home"))

    return render_template("register.html")

# ----------------- ADMIN DASHBOARD -----------------
@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if session.get("role") != "admin":
        flash("Access denied", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        # Update marks for all questions
        for q in Question.query.all():
            new_marks = request.form.get(f"marks_{q.id}")
            if new_marks:
                try:
                    q.marks = int(new_marks)
                except ValueError:
                    continue
        db.session.commit()
        flash("Marks updated successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    questions = Question.query.all()
    results = Result.query.all()  # now template will use r.user.username
    return render_template("admin.html", questions=questions, results=results)


# ----------------- ADD QUESTION -----------------
@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if session.get("role") != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        question_text = request.form.get("question")
        optionA = request.form.get("optionA")
        optionB = request.form.get("optionB")
        optionC = request.form.get("optionC")
        optionD = request.form.get("optionD")
        answer = request.form.get("answer")
        marks = int(request.form.get("marks", 1))

        new_q = Question(
            question=question_text,
            option_a=optionA,
            option_b=optionB,
            option_c=optionC,
            option_d=optionD,
            answer=answer,
            marks=marks
        )

        db.session.add(new_q)
        db.session.commit()
        flash("Question added successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_question.html")

# ----------------- EDIT QUESTION MARKS -----------------
@app.route("/admin/question/<int:q_id>/edit", methods=["GET", "POST"])
def edit_question(q_id):
    if session.get("role") != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    question = Question.query.get_or_404(q_id)

    if request.method == "POST":
        question.marks = int(request.form.get("marks", question.marks))
        db.session.commit()
        flash("Marks updated successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("edit_question.html", question=question)

# ----------------- START EXAM -----------------
@app.route("/exam", methods=["GET", "POST"])
def start_exam():
    if "user_id" not in session:
        flash("Please login first.", "danger")
        return redirect(url_for("home"))

    questions = Question.query.all()

    if request.method == "POST":
        total_score = 0
        total_marks = 0
        question_results = []

        for q in questions:
            user_answer = request.form.get(f"q{q.id}")
            total_marks += q.marks

            correct = (user_answer is not None) and (user_answer.upper() == q.answer.upper())
            if correct:
                total_score += q.marks

            question_results.append({
                "id": q.id,
                "question": q.question,
                "user_answer": user_answer,
                "correct_answer": q.answer,
                "marks": q.marks,
                "earned": q.marks if correct else 0
            })

        # Save result in DB
        result = Result(user_id=session["user_id"], score=total_score)
        db.session.add(result)
        db.session.commit()

        return render_template(
            "exam_result.html",
            question_results=question_results,
            total_score=total_score,
            total_marks=total_marks
        )

    return render_template("exam.html", questions=questions)


# ----------------- VIEW ALL RESULTS -----------------
@app.route("/admin/results")
def view_results():
    if session.get("role") != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    results = db.session.query(Result, User.username).join(User, User.id == Result.user_id).all()
    return render_template("admin_results.html", results=results)

# ----------------- LOGOUT -----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))


# ----------------- RUN APP -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
