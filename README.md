# Flask Server with User Database + Google Sheets Integration

This project is a **template web application** that sets up:  
✅ **A Python Flask server**  
✅ **Google Sheets API integration (with OAuth)**  
✅ **An SQLite3 user login + registration system**  

It’s designed as a fast-start boilerplate to connect a basic Python server with Google Workspace tools — letting you extend it into custom dashboards, automations, or data-driven apps.

---

## ✨ Features

- Secure Google OAuth flow for Sheets access  
- Reads and writes spreadsheet data in real time  
- Simple SQLite3-backed login and user management  
- Flask REST endpoints (separating backend and frontend)  
- Clear error flashing and feedback in the UI  
- Easily extendable (future: React frontend integration.)

---

## ⚙️ Tech Stack

- Python (Flask)  
- SQLite3
- Google Sheets API (with optional Google Drive API)  

---  

## 🚀 Setup & Usage

1️⃣ Clone the repo & install dependencies  

`git clone https://github.com/invisispider/python-google-sheets-server`  
`cd /path/to/project`  
`pip install pipenv`  
`pipenv install`  

2️⃣ Set up Google Cloud project

- Go to In the [Google Cloud Console](https://console.cloud.google.com/)  
- Create a **new project**  
- Enable the Google Sheets API (and optionally Google Drive API)  
- Configure OAuth consent + scopes  
- Download `client_secret.json` and place it in the local environment (for local development)  

3️⃣ Configure environment & database

- Set your .env variables (client IDs, secrets, etc.)  
- Initialize the SQLite3 database  

4️⃣ Run the Flask server

- `flask --app application run`  

5️⃣ Access the app

- Open `http://127.0.0.1:5000` in your browser  
- Use the provided buttons to test authorization, database, and Sheets interactions  

---

## 📸 Demo
![Server Screenshot](./Screenshot.png)

---

## 🛠 Notes

- Current setup is configured for local development; production (using WSGI) is commented out and will need adjustments.  
- Only test users (added in Google Cloud) can bypass app verification for unverified scopes.  
- Example Flask routes include:
`/authorize`, `/login`, `/logout`, `/users`, `/weekly-check`, `/sheets-json`  

---

## 💼 Freelance Applications

I build or adapt **custom solutions like this** for small teams who:  
- Juggle data across Google Sheets, CRMs, or ERPs  
- Need **automated** dashboards or reports    
- Want a clean, intuitive web interface to monitor KPIs and insights  

If you’re wasting time on manual data work, I can help streamline and automate your process.

---

## Contact

Want to collaborate or learn more?

- **GitHub:** [invisispider](https://github.com/invisispider)  
- **Upwork:** [My Upwork Profile](https://www.upwork.com/freelancers/~01527a09cdcfd75500)  
- **Website:** [steinunlimited.com](https://steinunlimited.com/)

--- 

## 🌐 My GitHub Portfolio

Check out my other highlighted projects:  
- [pdf-coa-to-csv](https://github.com/invisispider/pdf-coa-to-csv) – Python tools that read PDF test certificates  
- [web-scrape-realtors](https://github.com/invisispider/web-scrape-realtors) – Python web scraper for US realtors  
- [mfa-metrc-login](https://github.com/invisispider/mfa-metrc-login) – Automates Metrc MFA login with backup codes  
- [python-google-sheets-server](https://github.com/invisispider/python-google-sheets-server) – Flask server with Google API integration  
- [Stein-Unlimited](https://github.com/invisispider/Stein-Unlimited) – Personal Vue 3 web app with advanced features  
- [invisispider.github.io](https://github.com/invisispider/invisispider.github.io) – My portfolio site on GitHub Pages
