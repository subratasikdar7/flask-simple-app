from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Flask App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .links {
            margin-top: 30px;
            text-align: center;
        }
        .links a {
            display: inline-block;
            margin: 0 10px;
            padding: 10px 15px;
            background-color: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .links a:hover {
            background-color: #1e7e34;
        }
        #result {
            margin-top: 20px;
            padding: 15px;
            background-color: #e9ecef;
            border-radius: 5px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Simple Flask App! 🐍</h1>
        <p>Current time: {{ current_time }}</p>
        
        <div class="form-group">
            <label for="name">Enter your name:</label>
            <input type="text" id="name" placeholder="Your name here...">
            <button onclick="greetUser()">Greet Me!</button>
        </div>
        
        <div id="result"></div>
        
        <div class="links">
            <a href="/about">About</a>
            <a href="/api/status">API Status</a>
            <a href="/api/time">Current Time API</a>
        </div>
    </div>

    <script>
        function greetUser() {
            const name = document.getElementById('name').value;
            if (!name.trim()) {
                alert('Please enter your name!');
                return;
            }
            
            fetch('/api/greet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({name: name})
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `<h3>${data.message}</h3><p>Timestamp: ${data.timestamp}</p>`;
                resultDiv.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Something went wrong!');
            });
        }
    </script>
</body>
</html>
"""

ABOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - Simple Flask App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>About This App</h1>
        <p>This is a simple Flask web application that demonstrates:</p>
        <ul>
            <li>HTML templating with embedded CSS and JavaScript</li>
            <li>Form handling and user interaction</li>
            <li>RESTful API endpoints</li>
            <li>JSON responses</li>
            <li>Basic routing</li>
        </ul>
        <p>Built with Python Flask framework.</p>
        <p><a href="/">← Back to Home</a></p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HTML_TEMPLATE, current_time=current_time)

@app.route('/about')
def about():
    return render_template_string(ABOUT_TEMPLATE)

@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()
    name = data.get('name', 'Anonymous')
    return jsonify({
        'message': f'Hello, {name}! Welcome to our Flask app!',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'running',
        'message': 'Flask app is working properly!',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/time')
def api_time():
    return jsonify({
        'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'unix_timestamp': int(datetime.now().timestamp())
    })

if __name__ == '__main__':
    import os
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # In production, debug should be False
    debug_mode = os.environ.get('FLASK_ENV', 'production') != 'production'
    
    print(f"Starting Flask app on port {port}...")
    print(f"Debug mode: {debug_mode}")
    
    # Bind to 0.0.0.0 to make it accessible from outside container
    app.run(debug=debug_mode, host='0.0.0.0', port=port)