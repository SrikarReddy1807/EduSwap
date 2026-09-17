# EduSwap: Skill Based Matchmaking

> A campus-focused peer-to-peer skill exchange platform that connects students based on the skills they can teach and the skills they want to learn.

---

## Overview

EduSwap is a web-based peer learning platform designed to facilitate skill exchange among students within an engineering campus.

The platform allows students to create profiles, select the skills they can teach, specify the skills they want to learn, discover relevant peers, and request learning sessions.

The system provides a structured environment for students to share knowledge with their peers while also finding suitable students to learn from.

---

## Features

* Student Registration: Create an account using student information and login credentials.
* Student Login: Secure login using roll number and password.
* Profile Management: View and manage student profile information.
* Skill Selection: Select multiple skills that can be taught or learned.
* Skill-Based Matching: Find relevant peers based on selected skills.
* Peer Discovery: View students who can help with a desired skill.
* Session Requests: Send and receive peer-learning session requests.
* Session Scheduling: Select the skill, peer, date, and time for a learning session.
* Request Management: Accept or reject incoming session requests.
* Session Status: View the current status of requested sessions.
* Campus-Focused Platform: Designed for peer-to-peer learning within a specific academic community.

---

## Tech Stack

* Python
* Flask
* HTML5
* CSS3
* Jinja2
* SQLite
* Git
* GitHub

---

## Project Structure

```text
EduSwap/
│
├── static/
│   ├── logo.png
│   └── style.css
│
├── templates/
│   ├── chat.html
│   ├── dashboard.html
│   ├── layout.html
│   ├── login.html
│   ├── match.html
│   ├── register.html
│   └── sessions.html
│
├── app.py
├── check_db.py
├── db_setup.py
├── delete_profile.py
├── requirements.txt
└── .gitignore
```

---

## Database

EduSwap uses SQLite as its database.

The application manages three primary areas of data:

### Users

Stores student account information such as roll number and password.

### Skills

Stores the skills associated with each student, including the skills they can teach and the skills they want to learn.

### Sessions

Stores peer-learning session requests, including the learner, teacher, skill, scheduled time, and request status.

---

## How It Works

A student first registers and logs into the platform.

After logging in, the student can manage their profile and select:

* Skills they can teach
* Skills they want to learn

Based on these skill preferences, the student can discover relevant peers.

The student can then select a suitable peer and request a learning session by choosing the required skill and scheduling a suitable date and time.

The other student can review the request and either accept or reject it. The resulting session status is then displayed to the users.

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/SrikarReddy1807/EduSwap.git
```

### 2. Navigate to the Project Directory

```bash
cd EduSwap
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

```bash
python db_setup.py
```

### 5. Run the Flask Application

```bash
python app.py
```

### 6. Open the Application

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

---

## Application Modules

### Registration

Allows new students to create their EduSwap account.

### Login

Provides authentication using the registered roll number and password.

### Dashboard

Provides access to the main features of EduSwap.

### Profile

Allows students to view and manage their profile details and skill preferences.

### Skills

Allows students to select multiple skills they can teach and skills they want to learn.

### Find Peers

Helps students discover peers who possess the skills they are interested in learning.

### Session Requests

Allows students to send, receive, accept, reject, and track peer-learning session requests.

### Session Scheduling

Allows students to specify a date and time for a peer-learning session.

---

## Project Objectives

* Create a centralized platform for student-to-student skill exchange.
* Help students discover peers with relevant skills.
* Encourage collaborative and peer-driven learning.
* Provide an organized method for requesting and scheduling learning sessions.
* Maintain student profiles and skill preferences.
* Simplify the process of finding suitable learning partners within a campus.

---

## Future Scope

The platform can be further enhanced with:

* Real-time chat and messaging
* Peer ratings and feedback
* Notifications and session reminders
* Availability-based matchmaking
* Advanced recommendation algorithms
* Session history
* Administrative dashboard
* Enhanced authentication and security
* Cloud deployment
* Multi-campus support
* Mobile application

---

## Developer

**Srikar Reddy**

GitHub: https://github.com/SrikarReddy1807

Repository: https://github.com/SrikarReddy1807/EduSwap

---

## License

This project is developed for educational and academic purposes.
