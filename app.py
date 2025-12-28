import boto3
import pymysql
from flask import Flask, render_template, request

app = Flask(__name__)

# ---------- FETCH DB CREDENTIALS FROM SSM ----------
ssm = boto3.client("ssm", region_name="eu-north-1")  # Replace region

def get_parameter(name, with_decryption=False):
    response = ssm.get_parameter(Name=name, WithDecryption=with_decryption)
    return response['Parameter']['Value']

DB_HOST = get_parameter("/myapp/db/host")
DB_USER = get_parameter("/myapp/db/user")
DB_PASSWORD = get_parameter("/myapp/db/password", with_decryption=True)
DB_NAME = get_parameter("/myapp/db/name")

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
    app.run(host="0.0.0.0", port=5000, debug=True)

