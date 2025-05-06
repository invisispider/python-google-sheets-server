from flask import (
    Flask, jsonify, render_template, flash, redirect, url_for, session, logging, request, 
    render_template_string, make_response
)
from flask_sqlalchemy import SQLAlchemy
# import pandas as pd
# from logging import FileHandler, WARNING
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# file_handler = FileHandler('f_py_errorlog.txt')

# file_handler.setLevel(WARNING)
# app.logger.addHandler(WARNING)


### LOCAL DEVELOPMENT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

### REMOTE APP
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/html/python/site.db'


# Your secret key
app.secret_key = b'FFFFFFFFFF'


app.debug = True
db = SQLAlchemy(app)

GOOGLE_REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']



class Users(db.Model):
    __table_name__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20))
    email = db.Column(db.String(120))
    passw = db.Column(db.String(60))
    def __repr__(self):
        return '<users %r>' % self.uname
    def __init__(self, user_id, uname, email, passw):
        self.user_id = user_id
        self.uname = uname
        self.email = email
        self.passw = passw

class Sheets(db.Model):
    __table_name__ = 'sheets'
    table_id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.String(120))
    sheet_id = db.Column(db.String(120))
    title = db.Column(db.String(120))
    def __repr__(self):
        return '<sheets %r>' % self.title
    def __init__(self, table_id, drive_id, sheet_id, title):
        self.table_id = table_id
        self.drive_id = drive_id
        self.sheet_id = sheet_id
        self.title = title

# adds models to database
# db.create_all()

# @app.errorhandler(404)
# def page_not_found(e):
#     return("four oh four!")

@app.route("/")
def index():
    # if 'uname' in session:
    #     flash("Welcome " + session['uname'])     
    return render_template("base.html")

@app.route('/authorize')
def authorize():


    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )

    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    # You can store `state` in session if you want to validate later
    session['state'] = state
    return redirect(auth_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state')
    if not state:
        return 'Missing state in session', 400

    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        state=state,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)

    if not flow.credentials:
        return 'Failed to get credentials', 400

    credentials = flow.credentials

    # Example: save credentials to a file (for testing only, secure in production!)
    with open('token.json', 'w') as token_file:
        token_file.write(credentials.to_json())

    # Example: store in session (or securely in DB, production!)
    # session['credentials'] = {
    #     'token': credentials.token,
    #     'refresh_token': credentials.refresh_token,
    #     'token_uri': credentials.token_uri,
    #     'client_id': credentials.client_id,
    #     'client_secret': credentials.client_secret,
    #     'scopes': credentials.scopes
    # }

    return 'Authentication successful! You can close this window.'

@app.route("/users", methods=["GET"])
def users():
    if 'uname' in session:
        try:
            user_list = ["Joe", "Bob", "Mary", "Pendlesmythe"]
            user_list.append(session['uname'])
            # user_list = session.query(Users)
            # flash(session)
            return render_template("users.html", user_list = user_list)
        except Exception as e:
            return str(e)
    else:
        flash("Not Logged In!")
        return render_template("login.html")

@app.route("/checklist")
def checklist():
    # import gdrive_getchecklist
    import gdrive
    client = gdrive.client
    titles = client.spreadsheet_titles()
    # flash(titles)
    service = client.sheet.service
    # !ADD SPREADSHEET IDEA FOR TASK LIST
    spread_id = "1rcaetzpRIVd2Rr67plqlZbD1ncUJ2xJhunEDdZRK6HU"
    # !ADD RANGE NAME
    range_name = "'EXAMPLE'!B4:B"
    result = service.spreadsheets().values().get(
        spreadsheetId=spread_id, range=range_name).execute()
    grid_values = result['values']
    # df = pd.DataFrame(grid_values).style.hide_index()
    # # df = df.style.hide_index()
    # # df.drop(['None'], inplace=True)
    # html_df = df.to_html()
    # html_df = html_df.replace("<table>", "<table class='table table-dark")
    # resp = render_template_string(html_df)
    # # return render_template("weekly.html", result=html_df)
    return render_template("weekly.html", result=grid_values)

@app.route("/sheets-json")
def sheets_json():
    import gdrive
    client = gdrive.client
    titles = client.spreadsheet_titles()
    ids = client.spreadsheet_ids()
    sheets = zip(titles, ids)
    # drive_id = client.teamDriveId
    return render_template("sheets-json.html", sheets=sheets)

@app.route("/sheet/<sheets_id>/")
def display_json():
    return "sheets id"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        email = request.form['email']
        passw = request.form['passw']
        # if uname in ('Adam', 'Technomancer'):
            # flash('That name is spoilt. Use another.')
            # return render_template("register.html")
        if uname == 'Technomancer':
            flash('That is the one')
            # the auto-increment isn't happenin. todo: no manual user_id
            register = Users(user_id = 4, uname = uname, email = email, passw = passw)
            db.session.add(register)
            db.session.commit()
            flash('Technomancer added')
            return render_template("register.html")
            # return redirect(url_for("login"))
        else:
            flash('That user is not currently allowable')
            return render_template("register.html")
    else:
        if 'uname' in session:
            flash("logging out")
            session.pop("uname", None)
        flash("register page")
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("uname", None)
    flash("Logged Out")
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            uname = request.form["uname"]
            passw = request.form["passw"]
            login = Users.query.filter_by(uname=uname, passw=passw).first()
            if login is not None:
                session['uname'] = uname
                session['passw'] = passw
                flash("logged in.")
            else:
                flash("login failed")
            return render_template("login.html")
        else:
            return render_template("login.html")
    except Exception as e:
        flash(str(e))
        return render_template("base.html")

if __name__ == "__main__":
    # For Local Development
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    # For Remote
    # db.create_all()

