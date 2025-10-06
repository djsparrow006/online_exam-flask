from database import create_connection
from exam_logic import start_exam

def login():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Login successful! Welcome, {username}")
        return user
    else:
        print("❌ Invalid username or password.")
        return None

# Main
if __name__ == "__main__":
    user = login()
    if user:
        if user['role'] == 'student':
            start_exam(user)
        else:
            print("Admin logged in! Use admin panel to add/view questions.")
