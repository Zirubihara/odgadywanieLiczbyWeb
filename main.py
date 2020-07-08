import hashlib
import uuid

from flask import Flask, render_template, request, make_response, redirect, url_for
import random
from models import db, User

app = Flask(__name__)
db.create_all()

@app.route("/")
def index():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token = session_token).first()
    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    secret_number = random.randint(1, 30)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number, password=hashed_password)

        db.add(user)
        db.commit()

    if hashed_password != user.password:
        return "Nieprawidłowe hasło!!!"

    elif hashed_password==user.password:

        session_token = str(uuid.uuid4())


        user.session_token = session_token
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('index')))
        response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

        return response


@app.route("/profile")
def profile():
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token).first()

    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for("index"))


#www.mojastrona.pl/profile/edit - GET
#www.mojastrona.pl/profile/edit - POST

#PostMan

@app.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token).first()

    if request.method == "GET":
        if user:
            return render_template("profile_edit.html", user=user)
        else:
            return redirect(url_for("index"))
    elif request.method == "POST":
        name = request.form.get("profile-name")
        email = request.form.get("profile-email")

        user.name = name
        user.email = email

        db.add(user)
        db.commit()

        return redirect(url_for("profile"))


@app.route("/profile/delete", methods=["GET", "POST"])
def profile_delete():
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token).first()

    if request.method == "GET":
        if user:
            return render_template("profile_delete.html", user=user)
        else:
            return redirect(url_for("index"))
    elif request.method == "POST":
        db.delete(user)
        db.commit()

        return redirect(url_for("index"))

@app.route("/users")
def all_users():
    users = db.query(User).all()

    return render_template("users.html", users=users)

@app.route("/user/<user_id>")
def user_details(user_id):
    user = db.query(User).get(int(user_id))

    return render_template("user_details.html", user=user)



@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))

    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token= session_token).first()


    if guess == user.secret_number:
        message = "Udało Ci się odgadnąć liczbę!"

        new_secret = random.randint(1,30)

        user.secret_number = new_secret

        db.add(user)
        db.commit()

    elif guess > user.secret_number:
        message = "Twoja Liczba jest zbyt duza"
    elif guess < user.secret_number:
        message = "Twoja liczba jest zbyt mala"

    return render_template("result.html", message=message)

if __name__ == '__main__':
    app.run()