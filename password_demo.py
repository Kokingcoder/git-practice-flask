from werkzeug.security import generate_password_hash, check_password_hash

def demo():
    raw_password = "test1234"  # sample only, NOT a real password
    password_hash = generate_password_hash(raw_password)

    print("Raw password:", raw_password)
    print("Stored hash:", password_hash)

    print("Correct password check:", check_password_hash(password_hash, "test1234"))
    print("Wrong password check:", check_password_hash(password_hash, "nope123"))

if __name__ == "__main__":
    demo()