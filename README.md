# ITI-SummerTraining-FullStack-Crowdfunding

# Crowdfunding Website

A simple **crowdfunding platform** built with Django and PostgreSQL. Users can create projects, donate, comment, rate projects, and report inappropriate content. Project owners can track donations and project performance.

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/AfraimElkesEleia/ITI-SummerTraining-FullStack-Crowdfunding.git
cd ITI-SummerTraining-FullStack-Crowdfunding
```
```bash
python -m venv venv
# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
# Database settings fill them in .env file
NAME=your_db_name           # Name of your PostgreSQL database
USER=your_db_user           # PostgreSQL username
PASSWORD=your_db_password   # Password of pgAdmin/PostgreSQL user
HOST=localhost              # Database host (usually localhost)
PORT=5432                   # Database port (default 5432)

# Email settings (.env file)
EMAIL_HOST_USER=youremail@example.com     # Your Gmail address
EMAIL_HOST_PASSWORD=your_email_password   # Gmail App Password Creat it first
DEFAULT_FROM_EMAIL=youremail@example.com  # Same as your Gmail address
```
```bash
python manage.py makemigrations
python manage.py migrate
```

