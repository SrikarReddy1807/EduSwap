from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "eduswap_secret"

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users(roll TEXT PRIMARY KEY,password TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS skills(roll TEXT PRIMARY KEY,teach TEXT,learn TEXT)")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        learner TEXT,
        teacher TEXT,
        skill TEXT,
        time TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

init_db()

skills_list = [
"Python","Java","C","C++","C#","JavaScript","TypeScript","Go","Rust","Kotlin",
"Swift","PHP","R","MATLAB","Scala","Dart","SQL","MySQL","PostgreSQL","MongoDB",
"Oracle","SQLite","Redis","Firebase","HTML","CSS","Bootstrap","Tailwind CSS","React",
"Angular","Vue.js","Node.js","Express.js","Django","Flask","Spring Boot","ASP.NET",
"REST APIs","GraphQL","Microservices","Docker","Kubernetes","Git","GitHub","GitLab",
"Linux","Unix","Bash","PowerShell","Cloud Computing","AWS","Azure","GCP","DevOps",
"CI/CD","Jenkins","Terraform","Ansible","Cybersecurity","Ethical Hacking",
"Penetration Testing","Network Security","Cryptography","Data Structures",
"Algorithms","Object-Oriented Programming","Functional Programming",
"Software Engineering","Software Testing","Unit Testing","Selenium","Machine Learning",
"Deep Learning","Artificial Intelligence","Computer Vision","Natural Language Processing",
"TensorFlow","PyTorch","Data Science","Data Analysis","Big Data","Hadoop","Apache Spark",
"ETL","Data Warehousing","Blockchain","Solidity","IoT","Embedded Systems","Operating Systems",
"Computer Networks","System Design","Distributed Systems","Multithreading","Concurrency",
"API Development","Database Management","Linux Administration","Virtualization",
"Containerization","System Administration","Troubleshooting"
]

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        roll = request.form.get('roll')
        password = request.form.get('password')

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE roll=? AND password=?", (roll,password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = roll
            return redirect('/dashboard')
        else:
            error = "Invalid Roll Number or Password"

    return render_template("login.html", error=error)

from flask import flash

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        roll = request.form['roll']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE roll=?", (roll,))
        user = cur.fetchone()

        if user:
            flash("User already exists", "error")
            return render_template("register.html")

        cur.execute("INSERT INTO users VALUES (?,?)", (roll,password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if not session.get('user'):
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == 'POST':
        teach = ",".join(request.form.getlist("teach_skills"))
        learn = ",".join(request.form.getlist("learn_skills"))

        cur.execute("""
        INSERT INTO skills(roll,teach,learn)
        VALUES(?,?,?)
        ON CONFLICT(roll)
        DO UPDATE SET teach=excluded.teach, learn=excluded.learn
        """,(session['user'],teach,learn))

        conn.commit()

    cur.execute("SELECT teach,learn FROM skills WHERE roll=?", (session['user'],))
    skills = cur.fetchone()

    cur.execute("""
    SELECT teacher, skill, time
    FROM sessions
    WHERE learner=? AND status='Accepted'
    """,(session['user'],))
    my_sessions = cur.fetchall()

    conn.close()

    return render_template("dashboard.html",
                           skills=skills,
                           skills_list=skills_list,
                           my_sessions=my_sessions)

@app.route('/match')
def match():
    if not session.get('user'):
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT learn FROM skills WHERE roll=?", (session['user'],))
    result = cur.fetchone()

    if not result:
        return "<h3>Update skills first.</h3>"

    learn_skills = result[0].split(',')

    cur.execute("SELECT roll,teach FROM skills WHERE roll!=?", (session['user'],))
    peers = cur.fetchall()

    matched = []

    for peer in peers:
        teach_list = peer[1].split(',')
        common = [skill for skill in learn_skills if skill in teach_list]

        if common:
            matched.append((peer[0], common))

    conn.close()

    return render_template("match.html", peers=matched)

@app.route('/request_session', methods=['POST'])
def request_session():
    if not session.get('user'):
        return redirect('/login')

    teacher = request.form.get('teacher')
    skill = request.form.get('skill')
    date = request.form.get('date')
    time = request.form.get('time')

    datetime_value = f"{date} {time}"

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO sessions(learner,teacher,skill,time,status) VALUES(?,?,?,?,?)",
                (session['user'],teacher,skill,datetime_value,"Pending"))

    conn.commit()
    conn.close()

    return redirect('/match')

@app.route('/sessions')
def sessions():
    if not session.get('user'):
        return redirect('/login')

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT id, learner, teacher, skill, time, status
    FROM sessions
    WHERE teacher=? OR learner=?
    """, (session['user'], session['user']))

    requests = cur.fetchall()
    conn.close()

    return render_template("sessions.html", requests=requests)

@app.route('/update_session/<int:id>/<action>')
def update_session(id,action):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if action == "accept":
        cur.execute("UPDATE sessions SET status='Accepted' WHERE id=?", (id,))
    else:
        cur.execute("UPDATE sessions SET status='Rejected' WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/sessions')

@app.route('/chat/<peer>')
def chat(peer):
    if not session.get('user'):
        return redirect('/login')
    return render_template("chat.html", peer=peer)

@app.route('/send_message', methods=['POST'])
def send_message():
    sender = session.get('user')
    receiver = request.form.get('receiver')
    message = request.form.get('message')

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO messages(sender,receiver,message) VALUES(?,?,?)",
                (sender, receiver, message))

    conn.commit()
    conn.close()

    return "OK"

@app.route('/get_messages/<peer>')
def get_messages(peer):
    user = session.get('user')

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT sender, message FROM messages
    WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
    ORDER BY id ASC
    """,(user, peer, peer, user))

    msgs = cur.fetchall()
    conn.close()

    return jsonify({"messages": msgs})

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)