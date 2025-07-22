# app1/app.py - Simple Flask Web Server
from flask import Flask, jsonify, render_template_string
import os
import socket

app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>App 1 - Test Server</title>
    <style>
        body { font-family: Arial; margin: 40px; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); color: white; }
        .container { background: rgba(0,0,0,0.7); padding: 30px; border-radius: 10px; }
        .info { background: rgba(255,255,255,0.1); padding: 15px; margin: 10px 0; border-radius: 5px; }
        h1 { color: #ffeb3b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 App 1 - Frontend Application</h1>
        <div class="info">
            <strong>Purpose:</strong> This simulates a React/Vue.js frontend application
        </div>
        <div class="info">
            <strong>Server Info:</strong><br>
            Hostname: {{ hostname }}<br>
            Port: {{ port }}<br>
            Container: {{ container_id }}
        </div>
        <div class="info">
            <strong>Test URLs:</strong><br>
            <a href="/api/status" style="color: #ffeb3b;">GET /api/status</a><br>
            <a href="/api/data" style="color: #ffeb3b;">GET /api/data</a>
        </div>
        <p>✅ <strong>Subdomain routing is working!</strong></p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, 
                                hostname=socket.gethostname(),
                                port=os.getenv('PORT', '3000'),
                                container_id=socket.gethostname()[:12])

@app.route('/api/status')
def status():
    return jsonify({
        'app': 'Frontend App 1',
        'status': 'healthy',
        'hostname': socket.gethostname(),
        'port': os.getenv('PORT', '3000'),
        'message': 'App 1 is running successfully!'
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        'app': 'Frontend App 1',
        'data': [
            {'id': 1, 'name': 'Sample User 1', 'role': 'student'},
            {'id': 2, 'name': 'Sample User 2', 'role': 'teacher'},
            {'id': 3, 'name': 'Sample User 3', 'role': 'admin'}
        ],
        'timestamp': '2025-07-22T10:00:00Z'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'app': 'app1'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)