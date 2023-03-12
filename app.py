from flask import Flask , render_template , request ,send_from_directory,redirect,session
import os
from pyqrcode import QRCode
import pyqrcode
import png
from flask import url_for
from helpers import apology
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

db = SQL("sqlite:///qrify.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        if not request.form.get("name"):
            return apology("No username",900)
        elif not request.form.get("password"):
            return apology("Enter password",800)
        elif not request.form.get("confirm_password"):
            return apology("Enter password",800)

        if request.form.get("password") != request.form.get("confirm_password"):
            return apology("password and confirm password not same",750)

        username = request.form.get("name")
        pswd = request.form.get("password")
        password = generate_password_hash(pswd)

        #check if the username is already taken
        name=db.execute("SELECT * FROM users WHERE username=?",username)
        if len(name) == 1:
            return apology("username already exists", 400)

        # now we can store username and hashed password into sqlite database
        db.execute("INSERT INTO users (username,password) VALUES (?,?)",username,password)
        # find for the id of inserted user
        user_id = db.execute("SELECT id FROM users WHERE username = ?",username)
        print(user_id)
        # set the userid for entire session - as we will need the id of logged user later in other functions to execute queries
        # Session["user_id"]= db.execute("SELECT id FROM users WHERE username=?", username)
       
        session["user_id"]  = db.execute("SELECT id FROM users WHERE username=?", username)

        print("session id in register is :" + str(session["user_id"]))
        return render_template("check.html")
        # return redirect("/login")
        
@app.route("/qr/<path:filename>")
def serve_qr(filename):
    return send_from_directory(os.getcwd(), filename)


@app.route("/show")
def show():
    # print(session["user_id"])
    value = session["user_id"]
    id = value[0]['id']
    qrs = db.execute("SELECT qrname,qrdescription FROM qrinfo WHERE user_id = :userid;",userid = id)
    return render_template("showqr.html",qrs = qrs) 


@app.route("/login",methods=['GET','POST'])
def login():
    # Session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        # take username and pswd from form
        username = request.form.get("username")
        pswd = request.form.get("password")

        # check if password for that user is correct or not
      
        check_pswd = db.execute("SELECT password FROM users WHERE username = ?", username)
        # as check_pswd will be a list (since select method always returns a list) thus done the below step
        hashed_password = check_pswd[0]["password"]
        if not check_password_hash(hashed_password, pswd):
            return apology("Incorrect password for the username", 89)       
        else:
            # clear any previous sessions
            session.clear()
            session["user_id"] = db.execute("SELECT id FROM users WHERE username=?", username)
            return render_template("check.html")


# function to generate a QR from URL
def generate(url):
    qr_code = pyqrcode.create(url)
    
    with open("qr.png", "wb") as f:
        # img = qr_code.png(file: any, scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff,0xff])
        img = qr_code.png('qr.png',scale=8, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff,0xff])
        try:
            f.write(img)
        except Exception as e:
            print("Error writing image to file:", e)


    cwd = os.getcwd()
    image = 'qr.png'
    location = os.path.join(cwd,image)
    return location

    

@app.route("/check",methods=['GET','POST'])
def check():
    if request.method == "GET":
        return render_template("check.html")
    else:
        qrdescrpition = request.form.get("qrdescription")
        qrname = request.form.get("qrname")

        if not qrdescrpition or not qrname:
            return apology("Please enter URL and QR name",99)

        img_src = generate(qrdescrpition)
        print("img-src is :"+ img_src)

        # save the qr into database into the qrinfo table
        print("session id in check is :"+ str(session["user_id"]))
        value = session["user_id"]
        id = value[0]['id']
        # db.execute("INSERT INTO qrinfo(user_id,qrname,qrdescription) VALUES(:userid,:qrname,:qrdescr);",userid =session["user_id"],qrname = qrname,qrdescr = qrdescrpition)
        db.execute("INSERT INTO qrinfo(user_id,qrname,qrdescription) VALUES(:userid,:qrname,:qrdescr);",userid =id,qrname = qrname,qrdescr = qrdescrpition)

        # db.execute("INSERT INTO qrinfo(user_id,qrname,qrdescription) VALUES(?,?,?);",
        #    (id, qrname, qrdescrpition))

        return render_template("checked.html",image=img_src,name=qrname)



@app.route("/logout")
def logout():
      # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/info")
def info():
    return render_template("info.html")


