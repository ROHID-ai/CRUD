from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ----------- CREATE DATABASE -----------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            mobile INTEGER,
            city TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------- READ (HOME PAGE) -----------
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")   # SQL SELECT
    users = cur.fetchall()
    conn.close()
    return render_template("index.html", users=users)

# ----------- ADD USER -----------
@app.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form.get("mobile_no") or request.form.get("mobile")
        city = request.form["city"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, mobile, city) VALUES (?, ?, ?, ?)",  
            (name, email, mobile, city)
        )  # SQL INSERT
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("add.html")

# ----------- UPDATE USER -----------
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_user(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form.get("mobile_no") or request.form.get("mobile")
        city = request.form["city"]

        cur.execute(
            "UPDATE users SET name=?, email=?, mobile=?, city=? WHERE id=?",
            (name, email, mobile, city, id)
        )  # SQL UPDATE
        conn.commit()
        conn.close()
        return redirect("/")

    cur.execute("SELECT * FROM users WHERE id=?", (id,))  # SQL SELECT ONE
    user = cur.fetchone()
    conn.close()

    return render_template("update.html", user=user)

# ----------- DELETE USER -----------
@app.route("/delete/<int:id>")
def delete_user(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (id,))  # SQL DELETE
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)