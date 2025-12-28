from flask import Flask, render_template, request
import pymysql


app = Flask(__name__)

# ---------- DATABASE CONFIG ----------
<<<<<<< HEAD
DB_HOST = "/rds/endpoint/credentail"
DB_USER = "/rds/hostname/credentail"
DB_PASSWORD = "/rds/password/credentail"
DB_NAME = "/rds/username/credential"
=======
DB_HOST = "projectdb.ctwwe0s80yht.eu-north-1.rds.amazonaws.com"
DB_USER = "samidha"
DB_PASSWORD = "samidha12"
DB_NAME = "projectdb"
>>>>>>> d2977f99e353d9a62fd729bd7abc0274b3670c84


def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    conn.close()

    if result:
        return render_template("index.html", message="Login Successful")
    else:
        return render_template("index.html", message="Invalid Credentials")


# ---------- RUN APP ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
