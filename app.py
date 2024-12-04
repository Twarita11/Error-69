from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://twaritas4:hello1234@cluster0.bqpmw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = MongoClient(uri, server_api=ServerApi('1'))

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Parse JSON data from the request
        data = request.get_json()
        print(data)

        # Extract values from the JSON data
        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        parents_email_id = data.get('parents_email_id')
        parents_phone_number = data.get('parents_phone_number')

        # Validate fields
        if not name or not email or not age or not age.isdigit():
            return jsonify({"error": "Invalid data. 'name', 'email', 'parents_email_id', 'parents_phone_number' and 'age' are required."}), 400

        # Convert age to integer
        age = int(age)

        # Store data in MongoDB
        users_collection = mongo.db.users
        user_data = {
            "name": name,
            "email": email,
            "age": age,
            "parents_email_id": parents_email_id,
            "parents_phone_number": parents_phone_number
        }
        users_collection.insert_one(user_data)

        return jsonify({"message": "User data successfully stored in MongoDB"}), 201

@app.route('/profile', methods=['GET'])
def profile():
    """Fetch all user data from MongoDB and return it as JSON."""
    users_collection = mongo.db.users
    users = users_collection.find()  # Fetch all users

    # Convert users to a list of dictionaries
    users_list = []
    for user in users:
        user_dict = {
            "id": str(user["_id"]),  # Convert ObjectId to string for JSON serialization
            "name": user["name"],
            "email": user["email"],
            "age": user["age"],
            "parents_email_id": user["parents_email_id"],
            "parents_phone_number": user["parents_phone_number"]
        }
        users_list.append(user_dict)

    if users_list:
        return jsonify(users_list)
    else:
        return jsonify({"message": "No user data found"}), 404

@app.route('/')
def index():
    return render_template('sign.html')

# Initialize the app and run
if __name__ == '__main__':
    app.run(debug=True)
