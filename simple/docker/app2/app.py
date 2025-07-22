# app2/app.py - Simple API Server
from flask import Flask, jsonify, request, render_template_string
import os
import socket
import random
from datetime import datetime

app = Flask(__name__)

# Simple HTML template for API documentation
API_DOC_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>App 2 - API Server</title>
    <style>
        body { font-family: Arial; margin: 40px; background: linear-gradient(45deg, #667eea, #764ba2); color: white; }
        .container { background: rgba(0,0,0,0.7); padding: 30px; border-radius: 10px; }
        .endpoint { background: rgba(255,255,255,0.1); padding: 15px; margin: 10px 0; border-radius: 5px; }
        .method { color: #4caf50; font-weight: bold; }
        h1 { color: #ffeb3b; }
        code { background: rgba(0,0,0,0.5); padding: 2px 5px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔌 App 2 - API Server</h1>
        <p><strong>Server:</strong> {{ hostname }} | <strong>Port:</strong> {{ port }}</p>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/api/users</code><br>
            Returns list of users
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/api/users</code><br>
            Create a new user
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/api/stats</code><br>
            Returns server statistics
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/health</code><br>
            Health check endpoint
        </div>
        
        <p>✅ <strong>API Server is running!</strong></p>
    </div>
</body>
</html>
"""

# Sample data
users_db = [
    {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'role': 'admin'},
    {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'role': 'user'},
    {'id': 3, 'name': 'Carol Davis', 'email': 'carol@example.com', 'role': 'user'},
]

@app.route('/')
def home():
    return render_template_string(API_DOC_TEMPLATE,
                                hostname=socket.gethostname(),
                                port=os.getenv('PORT', '8000'))

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({
        'status': 'success',
        'data': users_db,
        'total': len(users_db),
        'server': socket.gethostname()
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_user = {
        'id': len(users_db) + 1,
        'name': data['name'],
        'email': data.get('email', ''),
        'role': data.get('role', 'user')
    }
    users_db.append(new_user)
    
    return jsonify({
        'status': 'success',
        'message': 'User created successfully',
        'data': new_user
    }), 201

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'server': {
            'hostname': socket.gethostname(),
            'port': os.getenv('PORT', '8000'),
            'uptime': 'Running',
            'timestamp': datetime.now().isoformat()
        },
        'database': {
            'total_users': len(users_db),
            'active_connections': random.randint(5, 50)
        },
        'performance': {
            'cpu_usage': f"{random.randint(10, 80)}%",
            'memory_usage': f"{random.randint(30, 90)}%",
            'disk_usage': f"{random.randint(20, 70)}%"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'app': 'api-server',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)