import os
from flask import (
    Flask, flash, render_template,
    session, request, url_for, redirect)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

# Config #

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Pages #


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/recipes')
def recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipe')
def recipe():
    return render_template('recipe.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    # Checks if the form method is POST.
    if request.method == "POST":

        # Finds the user in database.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # If the user is in database check the passwords match.
        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()

                # If password matches log user in, redirect to homepage.
                return redirect(url_for(
                    "index", username=session["user"]))

            # If not then return flash message for incorrect Username/password
            else:
                flash("Incorret Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/logout')
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    # Checks if the form method is POST.
    if request.method == "POST":

        # Finds the user in the mongo DB database.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # If the user exists, alert the customer this username is in use.
        if existing_user:
            flash("Sorry, this username already exists. Please try another")
            return redirect(url_for("register"))

        # Inserts new user to data if username is new.
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Thank you for sigining up.")
        return redirect(url_for(
            "index", username=session["user"]))

    return render_template("register.html")


@app.route('/profile/<username>')
def profile(username):


@app.route('/add-recipe')
def add_recipe():
    return render_template('add-recipe.html')


@app.route('/edit-recipe')
def edit_recipe():
    return render_template('edit-recipe.html')


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
