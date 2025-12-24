from flask import Flask, render_template, request
import pymysql
import boto3

app = Flask(__name__)

# ---------- FETCH DATABASE CREDENTIALS FROM SSM ----------
ssm = boto3.client("ssm", region_name="ap-south-1")  # replace with your region

def get_ssm_parameter(name):
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response['Parameter']['Value']

DB_HOST = get_ssm_parameter("my-endpoint-crendentail")
DB_USER = get_ssm_parameter("my-name")
DB_PASSWORD = get_ssm_parameter("my-db-password")
DB_NAME = get_ssm_parameter("my-db-name")

# ---------- DATABASE CONNECTION ----------
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
