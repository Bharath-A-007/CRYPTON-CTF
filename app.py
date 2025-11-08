from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('ctf.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, score INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS flags
                 (id INTEGER PRIMARY KEY, challenge TEXT, flag TEXT, points INTEGER)''')
    
    challenges = [
        ('0-dummy', 'CRYPTON{dummy_flag_123}', 10),
        ('1-observant', 'CRYPTON{m3t4d4t4_1s_c00l}', 25),
        ('3-base64', 'CRYPTON{base64_is_not_secure}', 50)
    ]
    
    c.executemany('INSERT OR IGNORE INTO flags (challenge, flag, points) VALUES (?, ?, ?)', challenges)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CRYPTON CTF Platform</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .challenge { border: 1px solid #ccc; padding: 15px; margin: 10px 0; border-radius: 5px; }
            button { background: #007cba; color: white; padding: 10px 15px; border: none; border-radius: 3px; cursor: pointer; }
            input { padding: 8px; margin: 5px; width: 250px; }
        </style>
    </head>
    <body>
        <h1>🚩 CRYPTON CTF Scoring Platform</h1>
        
        <div class="challenge">
            <h3>📋 How to Play:</h3>
            <ol>
                <li>Solve challenges on our <a href="https://bharath-a-007.github.io/CRYPTON-CTF/" target="_blank">GitHub Pages site</a></li>
                <li>Find flags in format: CRYPTON{...}</li>
                <li>Submit flags here to earn points</li>
            </ol>
        </div>

        <h2>Submit Flag</h2>
        <form action="/submit" method="post">
            <input type="text" name="username" placeholder="Your Name" required><br>
            <input type="text" name="flag" placeholder="CRYPTON{...}" required><br>
            <button type="submit">Submit Flag</button>
        </form>

        <p><a href="/leaderboard">View Leaderboard</a></p>

        <div style="margin-top: 30px; padding: 15px; background: #f5f5f5; border-radius: 5px;">
            <h3>📚 Current Challenges:</h3>
            <ul>
                <li>0 - Dummy Tutorial (10 points)</li>
                <li>1 - The Observant Eye (25 points) - Check image metadata</li>
                <li>3 - Base64 Isn't Encryption (50 points)</li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit_flag():
    username = request.form['username']
    submitted_flag = request.form['flag']
    
    conn = sqlite3.connect('ctf.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM flags WHERE flag=?", (submitted_flag,))
    flag_data = c.fetchone()
    
    if flag_data:
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        
        if user:
            c.execute("UPDATE users SET score = score + ? WHERE username=?", (flag_data[3], username))
        else:
            c.execute("INSERT INTO users (username, score) VALUES (?, ?)", (username, flag_data[3]))
        
        conn.commit()
        conn.close()
        return f'''
        <h2>✅ Correct Flag!</h2>
        <p>+{flag_data[3]} points added to {username}</p>
        <a href="/">← Back to Home</a> | 
        <a href="/leaderboard">View Leaderboard</a>
        '''
    else:
        conn.close()
        return f'''
        <h2>❌ Wrong Flag!</h2>
        <p>Try again!</p>
        <a href="/">← Back to Home</a>
        '''

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
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #f5f5f5; }
        </style>
    </head>
    <body>
        <h1>🏆 Leaderboard</h1>
        <table>
            <tr><th>Rank</th><th>Player</th><th>Score</th></tr>
    '''
    
    for rank, (username, score) in enumerate(leaders, 1):
        leaderboard_html += f"<tr><td>{rank}</td><td>{username}</td><td>{score}</td></tr>"
    
    leaderboard_html += '''
        </table>
        <br>
        <a href="/">← Back to Home</a>
    </body>
    </html>
    '''
    
    return leaderboard_html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
