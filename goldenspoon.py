from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database Connection
import mysql.connector
import os

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 3306))
)

cursor = db.cursor()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("registration.html")



# ---------------- LOGIN PAGE ----------------

@app.route("/loginpage")
def loginpage():
    return render_template("login.html")


# ---------------- LOGIN ----------------

@app.route("/loginpage", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    sql = "SELECT * FROM register WHERE EMAIL=%s AND PASSWORD=%s"

    cursor.execute(sql, (email, password))

    user = cursor.fetchone()

    if user:
        return """
        <script>
        alert('Login Successful');
        window.location='/index';
        </script>
        """
    else:
        return """
        <script>
        alert('Invalid Email or Password');
        window.history.back();
        </script>
        """
  # ---------------- REGISTRATION ----------------

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    reenter = request.form["reenter"]

    if password != reenter:
        return """
        <script>
        alert('Passwords do not match');
        window.history.back();
        </script>
        """

    sql = """
    INSERT INTO register
    (NAME, EMAIL, PASSWORD, REENTER_PASSWORD)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(sql, (name, email, password, reenter))
    db.commit()

    return """
    <script>
    alert('Registration Successful');
    window.location='/loginpage';
    </script>
    """



# ---------------- HOME PAGE ----------------

@app.route("/index")
def index():
    return render_template("index.html")


# ---------------- CONTACT PAGE ----------------

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "GET":
        return render_template("contact.html")

    fullname = request.form["fullname"]
    emailid = request.form["emailid"]
    phone = request.form["phonenumber"]
    subject = request.form["subject"]
    message = request.form["message"]

    sql = """
    INSERT INTO contactdetails
    (FULLNAME, EMAILID, PHONENUMBER, SUBJECT, MESSAGE)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (fullname, emailid, phone, subject, message))
    db.commit()

    return """
    <script>
    alert('Message Sent Successfully!');
    window.location='/contact';
    </script>
    """


# ---------------- TABLE BOOKING PAGE ----------------

@app.route("/tablebooking")
def tablebooking():
    return render_template("tablebooking.html")


# ---------------- BOOK TABLE ----------------

@app.route("/tablebooking", methods=["POST"])
def booktable():

    name = request.form["name"]
    email = request.form["emailid"]
    phone = request.form["phonenumber"]
    date = request.form["date"]
    time = request.form["time"]
    guest = request.form["noofguest"]
    request1 = request.form["request"]

    sql = """
    INSERT INTO tablebooking
    (FULLNAME, EMAIL, PHONENUMBER, DATE, TIME, NOOFGUEST, SPECIALREQUEST)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (name, email, phone, date, time, guest, request1))
    db.commit()

    return """
    <script>
    alert('Table Booked Successfully!');
    window.location='/tablebooking';
    </script>
    """



@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


if __name__ == "__main__":
    app.run(debug=True)