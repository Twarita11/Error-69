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
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Parse form data from the request
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')

        # Validate fields
        if not name or not email or not age or not age.isdigit():
            return jsonify({"error": "Invalid data. 'name', 'email', and 'age' are required."}), 400

        # Convert age to integer
        age = int(age)

        # Store data in the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', (name, email, age))
        conn.commit()
        conn.close()

        return jsonify({"message": "User data successfully stored"}), 201

# Initialize the database and run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
