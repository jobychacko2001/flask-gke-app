from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder=None)  # Disable default static folder

# Serve the index page
@app.route('/')
def index():
    frontend_path = os.path.join(os.getcwd(), 'frontend')
    return send_from_directory(frontend_path, 'index.html')

# Handle favicon requests
@app.route('/favicon.ico')
def favicon():
    return '', 204

# POST route to handle data submission
@app.route('/data', methods=['POST'])
def handle_data():
    data = request.json
    value1 = data.get('value1')
    value2 = data.get('value2')

    # Save to database (SQLite for simplicity)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS entries (value1 TEXT, value2 TEXT)")
    cursor.execute("INSERT INTO entries (value1, value2) VALUES (?, ?)", (value1, value2))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Data saved successfully!'})

if __name__ == '__main__':
    # Ensure the 'frontend' directory exists
    if not os.path.exists('frontend'):
        os.makedirs('frontend')
    app.run(host='0.0.0.0', port=5000)
