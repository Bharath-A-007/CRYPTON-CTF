from flask import Flask, request, render_template_string, jsonify
import sqlite3
import os
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'crypton_ctf_secret_key_2024'

# Initialize database
def init_db():
    conn = sqlite3.connect('ctf.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, score INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS flags
                 (id INTEGER PRIMARY KEY, challenge TEXT, flag TEXT, points INTEGER)''')
    
    # Add all challenges
    challenges = [
        ('0-tutorial', 'CRYPTON{dummy_flag_123}', 15),
        ('1-observant-eye', 'CRYPTON{m3t4d4t4_1s_c00l}', 25),
        ('2-robot-talk', 'CRYPTON{r0b0ts_t0_th3_r3scu3}', 35),
        ('3-base64', 'CRYPTON{base64_is_not_secure}', 50),
        ('4-source-code', 'CRYPTON{v13w_s0urc3_c0mm3nt}', 75),
        ('5-caesar-cipher', 'CRYPTON{the_code_is_3}', 100),
        ('6-cookie-monster', 'CRYPTON{c00k13_m0n5t3r_4t3_1t}', 125),
        ('7-secret-message', 'CRYPTON{h1dd3n_1n_pl41n_s1ght}', 175),
        ('8-api-adventure', 'CRYPTON{4p1_5_4r3_fun}', 200)
        ('9-mysterious-redirect', 'CRYPTON{url_m4nipul4t10n_ftw}', 350),
        ('10-sql-injection', 'CRYPTON{sql1_1nj3ct10n_m45t3r}', 350)    
    ]
    
    c.executemany('INSERT OR IGNORE INTO flags (challenge, flag, points) VALUES (?, ?, ?)', challenges)
    conn.commit()
    conn.close()

init_db()

# Main CTF Platform
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CRYPTON CTF Platform</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            max-width: 1000px; 
            margin: 0 auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin: 20px 0;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #343a40;
            margin-bottom: 10px;
        }
        .form-group {
            margin: 20px 0;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            margin: 10px 0;
            box-sizing: border-box;
        }
        input[type="text"]:focus {
            border-color: #007cba;
            outline: none;
        }
        .submit-btn {
            background: #28a745;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
        }
        .submit-btn:hover {
            background: #218838;
            transform: translateY(-2px);
        }
        .nav-links {
            text-align: center;
            margin: 20px 0;
        }
        .nav-links a {
            display: inline-block;
            margin: 0 10px;
            padding: 10px 20px;
            background: #6c757d;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #545b62;
        }
        .message {
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .challenge-info {
            background: #e7f3ff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .stats {
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚩 CRYPTON CTF Scoring Platform</h1>
            <p>Submit your flags and climb the leaderboard!</p>
        </div>

        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/leaderboard">Leaderboard</a>
            <a href="https://bharath-a-007.github.io/CRYPTON-CTF/" target="_blank">Challenges</a>
        </div>

        {% if message %}
        <div class="message {{ message_type }}">
            {{ message }}
        </div>
        {% endif %}

        <div class="challenge-info">
            <h3>📋 Available Challenges:</h3>
            <ul>
                <li><strong>0-Tutorial</strong> (15 pts) - Learn the basics</li>
                <li><strong>1-Observant Eye</strong> (25 pts) - Image metadata</li>
                <li><strong>2-Robot Talk</strong> (35 pts) - Web crawling</li>
                <li><strong>3-Base64</strong> (50 pts) - Encoding</li>
                <li><strong>4-Source Code</strong> (75 pts) - HTML inspection</li>
                <li><strong>5-Caesar Cipher</strong> (100 pts) - Cryptography</li>
                <li><strong>6-Cookie Monster</strong> (125 pts) - Browser storage</li>
                <li><strong>7-Secret Message</strong> (175 pts) - Steganography</li>
                <li><strong>8-API Adventure</strong> (200 pts) - API exploration</li>
            </ul>
            <p><a href="https://bharath-a-007.github.io/CRYPTON-CTF/" target="_blank">→ Go to Challenges Website</a></p>
        </div>

        <form action="/submit" method="post">
            <div class="form-group">
                <label for="username"><strong>Username:</strong></label>
                <input type="text" id="username" name="username" placeholder="Enter your username" required>
            </div>
            
            <div class="form-group">
                <label for="flag"><strong>Flag:</strong></label>
                <input type="text" id="flag" name="flag" placeholder="Enter flag: CRYPTON{...}" required>
            </div>

            <button type="submit" class="submit-btn">🚩 Submit Flag</button>
        </form>

        <div class="stats">
            <h3>📊 Quick Stats</h3>
            <p>Total Challenges: <strong>9</strong> | Total Points: <strong>800</strong></p>
            <p>Flag Format: <code>CRYPTON{example_flag}</code></p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit_flag():
    username = request.form['username']
    submitted_flag = request.form['flag']
    
    conn = sqlite3.connect('ctf.db')
    c = conn.cursor()
    
    # Check if flag is correct
    c.execute("SELECT * FROM flags WHERE flag=?", (submitted_flag,))
    flag_data = c.fetchone()
    
    if flag_data:
        challenge_name = flag_data[1]
        points = flag_data[3]
        
        # Check if user already solved this challenge
        c.execute('''CREATE TABLE IF NOT EXISTS submissions
                     (id INTEGER PRIMARY KEY, username TEXT, challenge TEXT, flag TEXT)''')
        
        c.execute("SELECT * FROM submissions WHERE username=? AND challenge=?", (username, challenge_name))
        existing_submission = c.fetchone()
        
        if existing_submission:
            conn.close()
            return render_template_string(HTML_TEMPLATE, 
                                       message=f"❌ You already solved {challenge_name}!", 
                                       message_type="error")
        
        # Record submission
        c.execute("INSERT INTO submissions (username, challenge, flag) VALUES (?, ?, ?)", 
                 (username, challenge_name, submitted_flag))
        
        # Update user score
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        
        if user:
            c.execute("UPDATE users SET score = score + ? WHERE username=?", (points, username))
        else:
            c.execute("INSERT INTO users (username, score) VALUES (?, ?)", (username, points))
        
        conn.commit()
        conn.close()
        
        return render_template_string(HTML_TEMPLATE, 
                                   message=f"✅ Correct! +{points} points for {challenge_name}. Total points added to {username}", 
                                   message_type="success")
    else:
        conn.close()
        return render_template_string(HTML_TEMPLATE, 
                                   message="❌ Wrong flag! Check the format: CRYPTON{...}", 
                                   message_type="error")

@app.route('/leaderboard')
def leaderboard():
    conn = sqlite3.connect('ctf.db')
    c = conn.cursor()
    c.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 20")
    leaders = c.fetchall()
    conn.close()
    
    leaderboard_html = '''
    <!DOCTYPE html>
    <html>
<head>
    <title>Leaderboard - CRYPTON CTF</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            max-width: 1000px; 
            margin: 0 auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }
        th {
            background-color: #343a40;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        tr:hover {
            background-color: #e9ecef;
        }
        .rank-1 { background-color: #fff3cd !important; font-weight: bold; }
        .rank-2 { background-color: #e9ecef !important; }
        .rank-3 { background-color: #f8d7da !important; }
        .nav-links {
            text-align: center;
            margin: 20px 0;
        }
        .nav-links a {
            display: inline-block;
            margin: 0 10px;
            padding: 10px 20px;
            background: #6c757d;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #545b62;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 CRYPTON CTF Leaderboard</h1>
            <p>Top 20 Participants</p>
        </div>

        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/leaderboard">Leaderboard</a>
            <a href="https://bharath-a-007.github.io/CRYPTON-CTF/" target="_blank">Challenges</a>
        </div>
        
        <table>
            <tr>
                <th>Rank</th>
                <th>Player</th>
                <th>Score</th>
            </tr>
    '''
    
    for rank, (username, score) in enumerate(leaders, 1):
        rank_class = f"rank-{rank}" if rank <= 3 else ""
        leaderboard_html += f'<tr class="{rank_class}"><td>{rank}</td><td>{username}</td><td>{score}</td></tr>'
    
    leaderboard_html += '''
        </table>
        
        <div style="text-align: center; margin-top: 30px; color: #6c757d;">
            <p>Total Challenges: 9 | Total Points Available: 800</p>
        </div>
    </div>
</body>
</html>
    '''
    
    return leaderboard_html

# API Route for Challenge 8
@app.route('/api/books/<book_id>')
def get_book(book_id):
    books = {
        '0': {
            'id': 0,
            'title': 'The Secret of APIs',
            'author': 'CTF Admin',
            'flag': 'CRYPTON{4p1_5_4r3_fun}',
            'description': 'A book about exploring APIs and finding hidden treasures!'
        },
        '1': {
            'id': 1,
            'title': 'Web Exploitation Guide',
            'author': 'Security Expert',
            'description': 'Learn how to find vulnerabilities in web applications'
        },
        '2': {
            'id': 2,
            'title': 'Cryptography Basics',
            'author': 'Cipher Master',
            'description': 'Introduction to encryption and decryption techniques'
        }
    }
    
    if book_id in books:
        return jsonify(books[book_id])
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/redirect')
def redirect_page():
    page = request.args.get('page', '')
    
    if page == 'secret':
        return '''
        <div style="text-align: center; padding: 50px;">
            <h1>🎉 Secret Page Found!</h1>
            <div style="background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0; display: inline-block;">
                <h2>🚩 Your Flag:</h2>
                <p style="font-family: monospace; font-size: 1.3em;">CRYPTON{url_m4nipul4t10n_ftw}</p>
            </div>
            <br>
            <a href="/">Back to CTF Platform</a>
        </div>
        '''
    else:
        return f'''
        <div style="text-align: center; padding: 50px;">
            <h1>Page: {page}</h1>
            <p>This is the {page} page. Nothing special here...</p>
            <p>Try different page parameters!</p>
            <a href="/">Back to CTF Platform</a>
        </div>
        '''

# Robots.txt for Challenge 2
@app.route('/robots.txt')
def robots_txt():
    return "User-agent: *\nDisallow: /secret-robot-area/\n"

# Secret area for Challenge 2
@app.route('/secret-robot-area/')
def secret_robot_area():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Secret Robot Area</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            .flag-box { background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; }
        </style>
    </head>
    <body>
        <h1>🤫 Secret Area Found!</h1>
        <p>Congratulations! You found the secret area meant only for robots!</p>
        <div class="flag-box">
            <h2>🚩 Your Flag:</h2>
            <p style="font-family: monospace; font-size: 1.2em;">CRYPTON{r0b0ts_t0_th3_r3scu3}</p>
        </div>
        <p><a href="/">← Back to CTF Platform</a></p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
