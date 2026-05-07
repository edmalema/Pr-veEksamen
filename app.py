from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector
from dotenv import find_dotenv, load_dotenv
from waitress import serve

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
    return render_template('ping.html', User = session["user"])


@app.route("/login", methods=["GET","POST"])
def Login():
    

    if request.method == "POST":
        Username = request.form['username']
        Password = request.form['password']

        #Defines the post as either a login or a sign up
        LoginSignUp = request.form['type']

        
        #Defines database and sql syntax
        db = get_db()
        cursor = db.cursor()
        sql = "INSERT INTO Users (username, password) VALUES (%s, %s)"
        val = (Username, Password)

        #Executes sql
        cursor.execute(sql, val)
        db.commit()
        print(cursor.rowcount, "record inserted.")
        cursor.close()

        session["user"] = Username
        return redirect("/ping")


    return render_template('Login.html')






if __name__ == '__main__':
    serve(app, host = '0.0.0.0', port = 5000)