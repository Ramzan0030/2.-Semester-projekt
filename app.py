from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "hemmelig"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("booking_system.db")
        try:
            connection.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            connection.commit()
        except sqlite3.IntegrityError:
            return "Email er allerede i brug"
        finally:
            connection.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("booking_system.db")
        user = connection.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        connection.close()

        if user:
            session["user_id"] = user[0]
            session["name"] = user[1]
            return redirect("/booking")
        else:
            return "Forkert email eller adgangskode"

    return render_template("login.html")


@app.route("/booking")
def booking():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("booking.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)