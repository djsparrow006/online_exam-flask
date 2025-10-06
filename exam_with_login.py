# exam_with_login.py

# Fake user database (username: password)
users = {
    "admin": "admin123",
    "dani": "dj",
    "st": "p",
}

# Questions
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A. Paris", "B. London", "C. Rome", "D. Berlin"],
        "answer": "A"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["A. 3", "B. 4", "C. 5", "D. 22"],
        "answer": "B"
    },
    {
        "question": "Which language is this project written in?",
        "options": ["A. C++", "B. Java", "C. Python", "D. Ruby"],
        "answer": "C"
    }
]

def login():
    print("=== Login Page ===")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username] == password:
        print(f" Login successful! Welcome, {username}\n")
        return username
    else:
        print("❌ Invalid username or password. Try again.")
        return None

def start_exam(username):
    print(f"=== Online Examination for {username} ===\n")
    score = 0

    for q in questions:
        print(q["question"])
        for option in q["options"]:
            print(option)
        answer = input("Your answer (A/B/C/D): ").strip().upper()

        if answer == q["answer"]:
            print(" Correct!\n")
            score += 1
        else:
            print(f" Wrong! Correct answer is {q['answer']}\n")

    print(f"{username}, your final score is {score}/{len(questions)}")

# Main Program
while True:
    user = login()
    if user:
        start_exam(user)
        break
