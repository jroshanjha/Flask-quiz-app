from werkzeug.security import generate_password_hash
import mysql.connector  # or sqlite3, depending on your DB


# Then you updated your code to hash passwords (e.g. pbkdf2:sha256) before saving them:

# from werkzeug.security import generate_password_hash, check_password_hash

# Now, your login function compares input passwords using:

# check_password_hash(stored_password, entered_password)

# ✅ Option 1: One-Time Migration (Recommended)

# Convert all existing plain-text passwords to hashed passwords in your database once.

# ⚡ Option 2: Backward Compatibility (Temporary Fix)

# If you can’t migrate all at once, handle both old and new formats in login:

from werkzeug.security import check_password_hash, generate_password_hash

def verify_password(stored_password, entered_password):
    # If stored password is plain text (no hashing)
    if not stored_password.startswith('pbkdf2:sha256'):
        return stored_password == entered_password
    # Otherwise, verify the hash
    return check_password_hash(stored_password, entered_password)

# Then in your login route:

# if verify_password(user['password'], form_password):
#     # login successful

# Later, you can automatically hash old passwords after successful login:

# if stored_password == entered_password:
#     hashed = generate_password_hash(entered_password)
#     cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed, user['id']))
#     conn.commit()

# 💡 Final Recommendation
# Run Option 1 (one-time hash migration) if possible.
# Keep Option 2 (dual check) temporarily if you have many old users still logging in.
    
# Connect to your database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jroshan@98",
    database="hospital"
)
cursor = conn.cursor(dictionary=True)

# Fetch all users
cursor.execute("SELECT id, password FROM users")
users = cursor.fetchall()

# Loop through and hash any plain-text passwords
for user in users:
    pwd = user['password']
    if not pwd.startswith('pbkdf2:sha256'):  # means it's still plain text
        hashed_pwd = generate_password_hash(pwd)
        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_pwd, user['id']))

conn.commit()
cursor.close()
conn.close()
print("✅ All passwords converted to hashed format successfully!")
