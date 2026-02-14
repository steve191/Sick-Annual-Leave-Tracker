#!/usr/bin/env python3
import string
import secrets
import db

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(chars) for _ in range(length))
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        if has_upper and has_lower and has_digit and has_special and len(password) >= 14:
            return password

def main():
    print("=" * 50)
    print("  Sick & Annual Leave Tracker - Installation")
    print("=" * 50)
    print()

    print("[1/2] Initializing database...")
    db.init_db()
    print("      Database initialized successfully.")
    print()

    existing = db.get_user('admin')
    if existing:
        print("[2/2] Admin user already exists.")
        print("      If you need to reset the password, delete the")
        print("      database file and run this script again.")
    else:
        password = generate_password()
        db.create_admin_user(password)
        print("[2/2] Admin user created.")
        print()
        print("-" * 50)
        print("  ADMIN LOGIN CREDENTIALS")
        print("-" * 50)
        print(f"  Username: admin")
        print(f"  Password: {password}")
        print("-" * 50)
        print()
        print("  IMPORTANT: Save this password now!")
        print("  You will be asked to change it on first login.")

    print()
    print("=" * 50)
    print("  Installation complete!")
    print("  Run the app with: python app.py")
    print("=" * 50)

if __name__ == '__main__':
    main()
