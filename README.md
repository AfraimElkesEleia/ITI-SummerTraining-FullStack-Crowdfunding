# ITI-SummerTraining-FullStack-Crowdfunding

# 🌍 Crowd-Funding Web Application  

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

> A web platform for starting and supporting fundraising projects in **Egypt**.  
This project allows users to create, donate, and manage fundraising campaigns while ensuring transparency, security, and user engagement.  

---
## 📌 About the Project  

Crowdfunding is the practice of raising small amounts of money from a large number of people, typically via the Internet.  
This project was developed to build a **fundraising platform in Egypt**, where users can:  
- Start fundraising campaigns  
- Donate to projects  
- Track donations and progress  

> In 2015, over **US$34 billion** was raised worldwide by crowdfunding (Wikipedia).  

---

## 🚀 Features  

### 1. Authentication System  
- **Registration** with fields:  
  - First name, Last name  
  - Email (unique)  
  - Password + Confirm password  
  - Mobile phone (validated against Egyptian numbers)  
  - Profile Picture  
- **Email Activation**  
  - User receives an email with an activation link.  
  - Account cannot be accessed until activated.  
  - Activation link expires after **24 hours**.  
- **Login** using email + password  
- **Bonus**: Login via Facebook  
- **Forgot Password** 
  - Password reset via email link.  
- **User Profile**  
  - View & update profile (except email).  
  - View projects & donations.  
  - Add extra optional info (Birthdate, Facebook profile, Country).  
  - Delete account with confirmation  
<img width="1920" height="1080" alt="Screenshot 2025-09-04 121635" src="https://github.com/user-attachments/assets/34a59fff-8ce2-4b1a-89eb-23af3c4946e2" />
<img width="1920" height="1080" alt="Screenshot 2025-09-04 121649" src="https://github.com/user-attachments/assets/f620146f-46f4-45b4-b5e8-b262a4db116d" />
<img width="1920" height="1080" alt="Screenshot 2025-09-04 121724" src="https://github.com/user-attachments/assets/43089c2e-e955-4651-9927-92fe40930e21" />
<img width="1920" height="1080" alt="Screenshot 2025-09-04 130912" src="https://github.com/user-attachments/assets/ecedbeaa-ff4b-4848-adc2-343cf9c8811a" />
<img width="1920" height="1080" alt="Screenshot (1)" src="https://github.com/user-attachments/assets/31771875-2422-41b9-8cb1-0861d7eb67c1" />
<img width="1920" height="1080" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/5b4b5445-47d5-4f9d-9743-337e7b18c889" />
<img width="1920" height="1080" alt="Screenshot (35)" src="https://github.com/user-attachments/assets/580ce8d4-bb63-46e1-841f-5c4ef2be5950" />
<img width="1920" height="1080" alt="Screenshot (36)" src="https://github.com/user-attachments/assets/4374e009-bbda-44ef-bdb7-75ac72cbd301" />
<img width="1920" height="1080" alt="Screenshot (37)" src="https://github.com/user-attachments/assets/f649792a-98fc-4b99-9691-e7d2346e84a5" />

---

### 2. Projects  
- Users can create fundraising campaigns with:  
  - Title  
  - Details  
  - Category (from admin-defined list)  
  - Multiple pictures  
  - Total target (e.g., `250000 EGP`)  
  - Multiple tags  
  - Start & end time  
- Project Features:  
  - Donations to project target.  
  - Comments (Bonus: replies to comments).  
  - Report inappropriate projects or comments.  
  - Rate projects (average rating displayed).  
  - Project creator can cancel if donations < 25% of target.  
  - Project page includes:  
    - Similar projects (based on tags).  
<img width="1920" height="1080" alt="Screenshot (19)" src="https://github.com/user-attachments/assets/951602a4-9afd-4674-a62c-c8b9c0520256" />
<img width="1920" height="1080" alt="Screenshot (22)" src="https://github.com/user-attachments/assets/34f8263a-1636-4ca8-9fbd-2331db52ae3c" />
<img width="1920" height="1080" alt="Screenshot (23)" src="https://github.com/user-attachments/assets/55beedd1-ecf6-47fb-adf4-f752322eeca1" />
<img width="1920" height="1080" alt="Screenshot (25)" src="https://github.com/user-attachments/assets/e957f412-6d8a-46cb-8a28-eb05ee094d66" />
<img width="1509" height="497" alt="Screenshot 2025-09-04 141439" src="https://github.com/user-attachments/assets/7b9d3ce2-d5a4-4e8a-9b51-8c2bef111b41" />
<img width="1477" height="288" alt="Screenshot 2025-09-04 141501" src="https://github.com/user-attachments/assets/38daa244-fabe-4fd0-9a41-1c4b5a4ad89a" />
<img width="1920" height="1080" alt="Screenshot (14)" src="https://github.com/user-attachments/assets/d673d1b5-982c-4e30-bbf5-8b6806a004a7" />
<img width="1920" height="1080" alt="Screenshot (15)" src="https://github.com/user-attachments/assets/c169de2c-d81d-48e5-9be1-cb31350e211b" />
<img width="1920" height="1080" alt="Screenshot (28)" src="https://github.com/user-attachments/assets/ecc52379-3d8d-4ef6-9759-456c4ad754fe" />
<img width="1920" height="1080" alt="Screenshot (29)" src="https://github.com/user-attachments/assets/18d81462-f2e6-45b0-a1e3-fcb5ce367ccf" />
<img width="1920" height="1080" alt="Screenshot (27)" src="https://github.com/user-attachments/assets/60cb8337-ff0c-4b56-904b-c457cf82a800" />

---
### 3. Homepage  
- **Highest-rated**: Top 5 highest-rated running projects.  
- **Latest Projects**: 5 newest projects.  
- **Featured Projects**: 5 admin-selected projects.  
- **Categories List**: Users can browse projects by category.  
- **Search Bar**: Search projects by title or tags.  
<img width="1920" height="1080" alt="Screenshot (24)" src="https://github.com/user-attachments/assets/87be4275-fb1e-4aee-9630-3259084f384b" />
<img width="1920" height="1080" alt="Screenshot (25)" src="https://github.com/user-attachments/assets/4c59a0d9-70a0-489e-a6d6-bf1230e62aa4" />
<img width="1889" height="927" alt="Screenshot 2025-09-04 140537" src="https://github.com/user-attachments/assets/070fdd7c-24d7-4086-a890-6bb82ae66d71" />
<img width="1892" height="926" alt="Screenshot 2025-09-03 131031" src="https://github.com/user-attachments/assets/0ec19df7-87b8-4534-8525-5dce0a5a541f" />
<img width="1920" height="1080" alt="Screenshot (12)" src="https://github.com/user-attachments/assets/80b8ae9d-9c15-4e56-a367-ca299ce6a20a" />

---

## 🛠 Tech Stack  

- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **Backend:** Django (Python)  
- **Database:** PostgreSQL / MySQL (choose depending on your implementation)  
- **Authentication:** Django built-in auth + Email verification  
- **Other Tools:**  
  - Pillow (image handling)  
  - Social Auth (for Facebook login)  

