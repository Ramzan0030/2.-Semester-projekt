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
            session["email"] = user[2]
     if email == "admin@dfa.dk":

        return redirect("/admin")

    else:

            return redirect("/booking")

        else:

            return "Forkert email eller adgangskode"

    return render_template("login.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        field = request.form["field"]
        trainer = request.form["trainer"]
        date = request.form["date"]
        time = request.form["time"]

        connection = sqlite3.connect("booking_system.db")

        connection.execute(
            """
            INSERT INTO bookings
            (user_id, trainer_id, field_id, booking_date, booking_time)

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                1,
                1,
                date,
                time
            )
        )

        connection.commit()
        connection.close()

        return render_template(
            "booking_success.html",
            field=field,
            trainer=trainer,
            date=date,
            time=time
        )

    return render_template("booking.html")


@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect("/login")

    if session["email"] != "admin@dfa.dk":
        return "Ingen adgang"

    connection = sqlite3.connect("booking_system.db")

    users = connection.execute(
        "SELECT id, name, email FROM users"
    ).fetchall()

    bookings = connection.execute(
        """
        SELECT id, booking_date, booking_time
        FROM bookings
        """
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        users=users,
        bookings=bookings
    )


@app.route("/delete_booking/<int:id>")
def delete_booking(id):

    connection = sqlite3.connect("booking_system.db")

    connection.execute(
        "DELETE FROM bookings WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)