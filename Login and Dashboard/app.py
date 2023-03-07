from flask import Flask, render_template, redirect, url_for, request # imports for flask
import sqlite3 # imports for SQL

app = Flask(__name__) # creating the flask app

# routes
@app.route('/') # linking a page to the home route "/"
def login():
    return render_template("login.html") # rendering the page that will be linked to the home url "/"

@app.route('/dashboard') # the first page after user logs in
def dashboard():
    return render_template("dashboard.html")

@app.route('/createlogindirect') # directing user from the login page to the create login page
def createloginredirect():
    return render_template("createlogin.html")


@app.route("/createlogin", methods = ["POST", "GET"]) # after the user as entered their detials in the create login page and excepting GET and POST requests
def createlogin():
    if request.method == "POST": # if a form is posting to the server:
        try:
            email = request.form["email"] # getting the values from the inputs with the name "email"
            password = request.form["password"]
            password1 = request.form["password1"]

            if password == password1: # if the passwords match:
                with sqlite3.connect("logins.db") as conn: # connecting to the database
                    cur = conn.cursor()
                    exists = cur.execute("SELECT * FROM logins WHERE email = (?)",(email,)).fetchall() # checking if the email exissts in the database
                    if len(exists) == 0: # if nothing is returned (it doesnt exist):
                        cur.execute("INSERT INTO logins (email,password) VALUES (?,?)", (email,password)) # insert the email and password combo
                        conn.commit() # save the chnages to the database
                        msg = "Account Successfuly Created"
                    else:
                        msg = "Email Already Exists"
            else:
                msg = "Passwords Do Not Match"
        except Exception as e: # general except statment to catch anything and print in command line
            print(e)
            msg = "Error in insert oporation"
        finally:
            if msg == "Account Successfuly Created": # if the account was created:
                return render_template("dashboard.html") # give access to database
            else:
                return render_template("result.html", msg = msg, func = "Account Creation") # if it wasn't successful, tell user

@app.route('/login', methods = ["POST", "GET"])
def commit_login():
    print(request.method)
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            
            if len(email) and len(password) > 0:  # making sure the user entered something in both fields
                with sqlite3.connect("logins.db") as conn:
                    cur = conn.cursor()
                    exists = cur.execute("SELECT * FROM logins WHERE email = (?)",(email,)).fetchall()
                    if len(exists) != 0 and (exists[0])[1] == password: # if the user entered something in the field and the second value in the list is equal to the password entered by the user
                        msg = "successful" # set message to successful
                    else:
                        msg = "Email or password incorrect" # if it isn't the same then set the message to an error message for the user
            else:
                msg = "Both fields must be filled in"
        except Exception as e:
            print(e)
        finally:
            if msg == "successful":
                return redirect(url_for("dashboard"))
            else:
                return render_template("result.html", msg = msg, func = "Loggin status")

if __name__ == "__main__":
    app.run(debug=True)