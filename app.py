from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector
from dotenv import find_dotenv, load_dotenv


app = Flask(__name__)

app.secret_key = "SuperSecretKey"
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
env_User = os.getenv("DB_USER")
env_Host = os.getenv("DB_HOST")
env_Password = os.getenv("DB_PASSWORD")
env_Database = os.getenv("DB_DATABASE")



def get_db():
    return mysql.connector.connect(
        host=env_Host,
        user=env_User,
        password=env_Password,
        database=env_Database
    )


@app.route("/ping", methods=["GET"])
def Ping():
    db = get_db()
    cursor = db.cursor


    return render_template('ping.html')