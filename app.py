from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
DATABASE = 'user_data.db'

def init_db():
    """Initialize the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            parents_email_id NOT NULL,
            parents_phone_number INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('http://127.0.0.1:5000//submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Parse form data from the request
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        parents_email_id = request.form.get('parents_email_id')
        parents_phone_number = request.form.get('parents_phone_number')

        # Validate fields
        if not name or not email or not age or not age.isdigit():
            return jsonify({"error": "Invalid data. 'name', 'email', 'parents_email_id', 'parents phone number' and 'age' are required."}), 400

        # Convert age to integer
        age = int(age)

        # Store data in the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, age, parents_email_id, parents_phone_number) VALUES (?, ?, ?, ?, ?)', (name, email, age, parents_email_id, parents_phone_number))
        conn.commit()
        conn.close()

        return jsonify({"message": "User data successfully stored"}), 201

@app.route('http://127.0.0.1:5000//profile', methods=['GET'])
def profile():
    """Fetch the user data from the database and return it as JSON."""
    # Get user data from the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, age, parents_email_id, parents_phone_number FROM users')
    rows = cursor.fetchall()  # Fetch all rows from the query
    
    conn.close()

    # If no users are found, return an empty list
    if not rows:
        return jsonify({"message": "No user data found"}), 404

    # Convert the data into a list of dictionaries for easy JSON conversion
    users = []
    for row in rows:
        user = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[3],
            "parents_email_id": row[4],
            "parents_phone_number": row[5]
        }
        users.append(user)

    return jsonify(users)

# Initialize the database and run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
