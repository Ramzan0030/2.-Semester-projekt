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

        training = request.form["training"]

        trainer, time = training.split("|")

        date = request.form["date"]

        connection = sqlite3.connect("booking_system.db")

        count = connection.execute(
            """
            SELECT COUNT(*)

            FROM bookings

            WHERE trainer_name = ?
            AND booking_date = ?
            AND booking_time = ?
            """,
            (trainer, date, time)
        ).fetchone()[0]

        if count >= 5:

            connection.close()

            return "Holdet er fyldt"

        connection.execute(
            """
            INSERT INTO bookings
            (user_id, trainer_name, booking_date, booking_time)

            VALUES (?, ?, ?, ?)
            """,
            (
                session["user_id"],
                trainer,
                date,
                time
            )
        )

        connection.commit()

        trainings = [

            ("Mustafa Baskaya", "12:00"),

            ("Muzaffer Celik", "14:00"),

            ("Mehmet Dagli", "16:00")

        ]

        training_data = []

        for trainer_name, training_time in trainings:

            booked = connection.execute(
                """
                SELECT COUNT(*)

                FROM bookings

                WHERE trainer_name = ?
                AND booking_time = ?
                """,
                (trainer_name, training_time)
            ).fetchone()[0]

            remaining = 5 - booked

            training_data.append(
                (trainer_name, training_time, remaining)
            )

        connection.close()

        remaining = 5 - (count + 1)

        return render_template(
            "booking_success.html",
            trainer=trainer,
            date=date,
            time=time,
            remaining=remaining
        )

    trainings = [

        ("Mustafa Baskaya", "12:00"),

        ("Muzaffer Celik", "14:00"),

        ("Mehmet Dagli", "16:00")

    ]

    training_data = []

    connection = sqlite3.connect("booking_system.db")

    for trainer, time in trainings:

        count = connection.execute(
            """
            SELECT COUNT(*)

            FROM bookings

            WHERE trainer_name = ?
            AND booking_time = ?
            """,
            (trainer, time)
        ).fetchone()[0]

        remaining = 5 - count

        training_data.append(
            (trainer, time, remaining)
        )

    connection.close()

    return render_template(
        "booking.html",
        trainings=training_data
    )


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
        SELECT
            bookings.id,
            users.name,
            trainer_name,
            booking_date,
            booking_time

        FROM bookings

        JOIN users
        ON bookings.user_id = users.id
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