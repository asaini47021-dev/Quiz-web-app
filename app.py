from flask import Flask, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)

# आपका MongoDB कनेक्शन (टाइमआउट सेटिंग्स के साथ ताकि हैंग न हो)
MONGO_URI = 'mongodb+srv://ssaini47021_db_user:jhJd1y4EeIPRk81K@cluster0.vuh9kkg.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client['QuizBotPro']
scores_db = db['scores']

# वेबसाइट का शानदार UI डिज़ाइन (Telegram Theme)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pro Quiz Leaderboard</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--tg-theme-bg-color, #18222d);
            color: var(--tg-theme-text-color, #ffffff);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: var(--tg-theme-secondary-bg-color, #242f3d);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }
        h2 {
            text-align: center;
            color: var(--tg-theme-button-color, #2ea6ff);
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }
        .user-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 10px;
            border-bottom: 1px solid #333;
            font-size: 18px;
        }
        .user-row:last-child { border-bottom: none; }
        .rank-1 { font-weight: bold; color: #FFD700; font-size: 20px; }
        .rank-2 { font-weight: bold; color: #C0C0C0; font-size: 19px; }
        .rank-3 { font-weight: bold; color: #cd7f32; font-size: 19px; }
        .score-box { background: var(--tg-theme-button-color, #2ea6ff); color: #fff; padding: 3px 10px; border-radius: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🏆 Global Quiz Leaderboard</h2>
        <div id="leaderboard">
            {% for user in users %}
            <div class="user-row">
                <span class="{% if loop.index == 1 %}rank-1{% elif loop.index == 2 %}rank-2{% elif loop.index == 3 %}rank-3{% endif %}">
                    {% if loop.index == 1 %}🥇{% elif loop.index == 2 %}🥈{% elif loop.index == 3 %}🥉{% else %}{{ loop.index }}.{% endif %} 
                    {{ user.name }}
                </span>
                <span class="score-box">{{ user.score }} Pts</span>
            </div>
            {% endfor %}
            {% if not users %}
            <p style="text-align:center; color:#888;">No scores yet. Play a quiz in the group to get ranked!</p>
            {% endif %}
        </div>
    </div>
    <script>
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        # डेटाबेस सेफली फेच करना
        users_cursor = scores_db.find().sort('score', -1).limit(50)
        users = list(users_cursor)
    except Exception as e:
        users = []
    return render_template_string(HTML_TEMPLATE, users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
