# app3/app.py - Simple Admin Panel
from flask import Flask, jsonify, render_template_string
import os
import socket
import random
from datetime import datetime

app = Flask(__name__)

# Admin dashboard template
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>App 3 - Admin Panel</title>
    <style>
        body { font-family: Arial; margin: 40px; background: linear-gradient(45deg, #11998e, #38ef7d); color: white; }
        .container { background: rgba(0,0,0,0.8); padding: 30px; border-radius: 10px; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }
        .metric { font-size: 2em; color: #ffeb3b; margin: 10px 0; }
        h1 { color: #ffeb3b; text-align: center; }
        h3 { color: #4caf50; }
        .status-ok { color: #4caf50; }
        .status-warning { color: #ff9800; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Admin Dashboard</h1>
        <p style="text-align: center;"><strong>Server:</strong> {{ hostname }} | <strong>Port:</strong> {{ port }}</p>
        
        <div class="dashboard">
            <div class="card">
                <h3>System Status</h3>
                <div>CPU Usage: <span class="metric">{{ cpu_percent }}%</span></div>
                <div>Memory: <span class="metric">{{ memory_percent }}%</span></div>
                <div>Status: <span class="status-ok">✅ Healthy</span></div>
            </div>
            
            <div class="card">
                <h3>Application Metrics</h3>
                <div>Active Users: <span class="metric">{{ active_users }}</span></div>
                <div>Total Requests: <span class="metric">{{ total_requests }}</span></div>
                <div>Uptime: <span class="metric">{{ uptime }}</span></div>
            </div>
            
            <div class="card">
                <h3>Quick Actions</h3>
                <p><a href="/admin/logs" style="color: #ffeb3b;">📋 View Logs</a></p>
                <p><a href="/admin/users" style="color: #ffeb3b;">👥 Manage Users</a></p>
                <p><a href="/admin/settings" style="color: #ffeb3b;">⚙️ Settings</a></p>
            </div>
        </div>
        
        <p style="text-align: center; margin-top: 30px;">✅ <strong>Admin panel is operational!</strong></p>
    </div>
</body>
</html>
"""

def get_system_info():
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        return {
            'cpu_percent': round(cpu_percent, 1),
            'memory_percent': round(memory.percent, 1)
        }
    except:
        # Fallback if psutil is not available
        return {
            'cpu_percent': round(random.uniform(10, 80), 1),
            'memory_percent': round(random.uniform(30, 90), 1)
        }

@app.route('/')
def dashboard():
    system_info = get_system_info()
    return render_template_string(ADMIN_TEMPLATE,
                                hostname=socket.gethostname(),
                                port=os.getenv('PORT', '5000'),
                                cpu_percent=system_info['cpu_percent'],
                                memory_percent=system_info['memory_percent'],
                                active_users=247,
                                total_requests=1543,
                                uptime='2d 14h 32m')

@app.route('/admin/logs')
def logs():
    sample_logs = [
        {'timestamp': '2025-07-22 10:30:15', 'level': 'INFO', 'message': 'User login successful: alice@example.com'},
        {'timestamp': '2025-07-22 10:28:42', 'level': 'WARN', 'message': 'High CPU usage detected: 85%'},
        {'timestamp': '2025-07-22 10:25:33', 'level': 'INFO', 'message': 'Database backup completed'},
        {'timestamp': '2025-07-22 10:20:11', 'level': 'ERROR', 'message': 'Failed login attempt: invalid password'},
        {'timestamp': '2025-07-22 10:15:07', 'level': 'INFO', 'message': 'System health check passed'},
    ]
    
    return jsonify({
        'status': 'success',
        'logs': sample_logs,
        'total': len(sample_logs),
        'server': socket.gethostname()
    })

@app.route('/admin/users')
def users():
    return jsonify({
        'status': 'success',
        'users': [
            {'id': 1, 'name': 'Admin User', 'role': 'admin', 'last_login': '2025-07-22 09:30:00'},
            {'id': 2, 'name': 'John Doe', 'role': 'user', 'last_login': '2025-07-22 08:45:00'},
            {'id': 3, 'name': 'Jane Smith', 'role': 'moderator', 'last_login': '2025-07-21 16:20:00'},
        ],
        'total_users': 3,
        'active_sessions': 12
    })

@app.route('/admin/settings')
def settings():
    return jsonify({
        'status': 'success',
        'settings': {
            'maintenance_mode': False,
            'debug_enabled': True,
            'max_concurrent_users': 1000,
            'session_timeout': 3600,
            'backup_frequency': 'daily',
            'log_level': 'INFO'
        }
    })

@app.route('/health')
def health():
    system_info = get_system_info()
    return jsonify({
        'status': 'ok',
        'app': 'admin-panel',
        'version': '1.0.0',
        'system': system_info,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)