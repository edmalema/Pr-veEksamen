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
        database=env_Database,
        #Forces mysql-connector-python to use its pure Python implementation instead of the C extension.
        use_pure=True
    )


@app.route("/index", methods=["GET"])
def Insdex():
    return render_template('Index.html', User = session["user"])


@app.route("/signup", methods=["GET","POST"])
def SignUp():
    if request.method == "POST":
        Username = request.form['username']
        Password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)



        #Checks if user already exist
        cursor.execute("SELECT * FROM Users WHERE username=%s", (Username,))
        user = cursor.fetchone()
        if (user != None):
            return render_template('SignUp.html', ErrorType = "User already exist")


        #Inserts new user
        cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (Username, Password))
        db.commit()
        cursor.close()

        session["user"] = Username
        return redirect("/ping")


    return render_template('SignUp.html', ErrorType = "")



@app.route("/login", methods=["GET","POST"])
def Login():
    if request.method == "POST":
        Username = request.form['username']
        Password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        #Gets the user
        #Checks if user exists, if the password is correct and if the user is active
        cursor.execute("SELECT * FROM Users WHERE username=%s", (Username,))
        user = cursor.fetchone()
        if user and user["password"] == Password:
            session['user'] = Username
            db.commit()
            cursor.close()

            session["user"] = Username
            return redirect("/index")
        else:
            return render_template('Login.html', ErrorType = "Incorrect username or password")

    return render_template('Login.html', ErrorType = "")



#Waitress
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080, threads=4)


#if __name__ == '__main__':
#    serve(app, host = '0.0.0.0', port = 5000)