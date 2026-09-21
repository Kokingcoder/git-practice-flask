from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

DB_PATH = "app.db"

def main():
    email = "demo@example.com"
    name = "Demo User"
    raw_password = "test1234"  # sample only

    password_hash = generate_password_hash(raw_password)
    print("Raw password:", raw_password)
    print("Password hash to store:", password_hash)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Clean up any old demo row
    cur.execute("DELETE FROM users WHERE email = ?", (email,))

    # Insert user with ONLY the hash stored
    cur.execute(
        "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
        (email, name, password_hash),
    )
    conn.commit()

    # Read it back
    cur.execute("SELECT id, email, name, password_hash FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    print("\nRow from DB:")
    print(row)

    stored_hash = row[3]
    print("\nCheck correct password:", check_password_hash(stored_hash, "test1234"))
    print("Check wrong password:", check_password_hash(stored_hash, "wrongpass"))

if __name__ == "__main__":
    main()