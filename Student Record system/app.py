from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
@app.route("/enternew")
def new_student():
    return render_template("student.html")

@app.route("/addrec", methods = ["POST", "GET"])
def addrec():
    if request.method == "POST":
        try:
            name = request.form["name"]
            id = request.form["id"]
            addr = request.form["add"]
            city = request.form["city"]

            with sqlite3.connect("Students.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO students (name,id,addr,city) VALUES (?,?,?,?)", (name,id,addr,city))
                conn.commit()
                msg = "Record Successfuly Added"
        except Exception as e:
            print(e)
            msg = "Error in insert oporation"
        finally:
            return render_template("result.html", msg = msg, func = "addition")

@app.route('/liststudents')
def listStudents():
    with sqlite3.connect("students.db") as conn:
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("SELECT * from students")
        rows = cur.fetchall()
    return render_template("studentlist.html", rows = rows)

@app.route("/searchrec", methods = ["POST", "GET"])
def searchrec():
    if request.method == "POST":
        try:
            name = request.form["search_name"]

            with sqlite3.connect("Students.db") as conn:
                cur = conn.cursor()
                msg = cur.execute("SELECT * FROM students WHERE name = (?)", (name,)).fetchall()

        except Exception as e:
            print(e)

        finally:
            return render_template("searchresult.html", msg = msg, func = "search")

@app.route('/commitchanges', methods=["POST","GET"])
def commitchanges():
    if request.method == "POST":
        try:
            edit_id = request.form["edit_id"]
            edit_name = request.form["edit_name"]
            edit_address = request.form["edit_address"]
            edit_city = request.form["edit_city"]
            
            with sqlite3.connect("Students.db") as conn:
                cur = conn.cursor()
                cur.execute("UPDATE Students SET name = (?), id = (?), addr = (?), city = (?) WHERE id = (?)", (edit_name, edit_id,edit_address, edit_city, edit_id))
                conn.commit()
                msg = "Database changes successfuly commited!"
        except Exception as e:
            msg = f"Problem finding ID [{e}]"
        finally:
            return render_template("result.html", func = "database edit", msg = msg)


@app.route('/editrec', methods=["POST","GET"])
def editrec():
    if request.method == "POST":
        try:
            original_id = request.form["edit_id"]
            
            with sqlite3.connect("Students.db") as conn:
                cur = conn.cursor()
                msg = cur.execute("SELECT * FROM students WHERE id = (?)", (original_id,)).fetchall()
        except Exception as e:
            msg = f"Problem finding ID [{e}]"
        finally:
            return render_template("editresult.html", func = "database edit", msg = msg)
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search')
def search():
    return render_template("search.html")
    
@app.route('/edit')
def edit():
    return render_template("edit.html")

if __name__ == "__main__":
    app.run(debug=True)

