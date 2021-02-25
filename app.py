import os
from flask import (
    Flask, flash, render_template,
    session, request, url_for, redirect)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from functools import wraps
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


def login_required(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if 'user' not in session:
            flash("Please login to your account first")
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)
    return login_check


# Homepage #


@app.route('/')
def index():
    return render_template("index.html")


# Recipe functions #


@app.route('/recipes')
def recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template('recipes.html', recipes=recipes)


@app.route('/search', methods=["GET", "POST"])
def search():
    """
    Searches the recipe index.
    Will return results for, Recipe name,
    description and ingredients.
    """
    query = request.form.get("search-query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))

    return render_template("recipes.html", recipes=recipes)


@app.route('/recipe/<recipe_id>')
def recipe_page(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)


# Login / register function #


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

                # If password matches log user in, direct to profile.
                return redirect(url_for(
                    "profile", username=session["user"]))

            # If password is wrong return flash message
            else:
                flash("Incorret Username and/or Password")
                return redirect(url_for("login"))
        # If not existing user return flash message
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/logout')
def logout():
    flash("Goodbye! You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    # Checks if the form method is POST.
    if request.method == "POST":

        # Finds the user in the mongo DB database.
        existing_username = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # Finds the email in the mongo DB database.
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        # If user exists, alert the customer this username is in use.
        if existing_username:
            flash("Sorry, this username already exists. Please try another")
            return redirect(url_for("register"))

        # If email has been used, alert the customer this email already in use.
        if existing_email:
            flash("Sorry, this email is in use. Please try another")
            return redirect(url_for("register"))

        # Inserts register dict to data if username is new.
        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Thank you for sigining up.")
        return redirect(url_for(
            "profile", username=session["user"]))

    return render_template("register.html")

# User logged in functions #


@app.route('/profile/<username>', methods=["GET", "POST"])
@login_required
def profile(username):
    """
    If the user has added recipes then
    they will display on profile page.
    """
    if session["user"] == "admin":
        recipes = list(mongo.db.recipes.find())
    else:
        recipes = list(mongo.db.recipes.find({"created_by": username.lower()}))
    return render_template("profile.html", recipes=recipes, username=username)

    return redirect(url_for("login"))


@app.route('/add-recipe', methods=["GET", "POST"])
def add_recipe():
    """
    Add recipe function allows the
    user to add their own recipes if logged in
    """
    if request.method == "POST":
        recipe = {
            "meal_name": request.form.get("meal_name"),
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.get("ingredients"),
            "description": request.form.get("description"),
            "recommendation": request.form.get("recommendation"),
            "yield": request.form.get("yield"),
            "active_time": request.form.get("active_time"),
            "total_time": request.form.get("total_time"),
            "img_url": request.form.get("img_url"),
            "method": request.form.get("method"),
            "created_by": session["user"]
        }

        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Succesfully Added")
        return redirect(url_for("recipes"))

    return render_template('add-recipe.html')


@app.route('/edit-recipe/<recipe_id>', methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Edit recipe function allows the
    user to edit their own recipes from
    their profile page.
    """
    if request.method == "POST":
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)},
            {'$set': {
                "meal_name": request.form.get("meal_name"),
                "recipe_name": request.form.get("recipe_name"),
                "ingredients": request.form.get("ingredients"),
                "description": request.form.get("description"),
                "recommendation": request.form.get("recommendation"),
                "yield": request.form.get("yield"),
                "active_time": request.form.get("active_time"),
                "total_time": request.form.get("total_time"),
                "img_url": request.form.get("img_url"),
                "method": request.form.get("method"),
                "created_by": session["user"]
            }})
        flash("Recipe Updated")
        return redirect(url_for("recipes"))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('edit-recipe.html', recipe=recipe)


@app.route('/delete-recipe/<recipe_id>')
def delete_recipe(recipe_id):
    """
    Delete function removes recipe
    from database and recipes page.
    """
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe removed")
    return redirect(url_for("recipes"))


# @app.route('/delete-account/<username>')
# def delete_user(username):
#     """
#     Delete user function removes user.(not used yet)
#     """
#     mongo.db.users.remove({"username": username.lower()})
#     flash("Sorry to see you go! Your user has been deleted")
#     return redirect(url_for("login"))


# @app_route('/subscribe', methods=["GET", "POST"])
# def subscribe_user():
#     subscription = {"email": request.form.get("email").lower()}
#     mongo.db.subscribers.insert_one(subscription)
#     return redirect(request.referrer)


# Error Pages #

"""
Return error pages if page not
found/Internal server error.
"""


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('/errors/500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
