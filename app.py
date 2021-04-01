import os
from flask import (
    Flask, flash, render_template,
    session, request, url_for, redirect)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from functools import wraps
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


# Config #

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)

mongo = PyMongo(app)


# Global variables used throughout functions #

default_pic = ("/static/images/default-profile-picture.jpg")
date = date.today()
recipes_data = mongo.db.recipes
users_data = mongo.db.users
subscribers_data = mongo.db.subscribers


def login_required(f):
    """
    Decorator for to be called on views that require users to be logged in.
    """

    @wraps(f)
    def login_check(*args, **kwargs):
        if 'user' not in session:
            flash("You need to login first!")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return login_check


# Homepage #

@app.route('/')
def index():
    return render_template("index.html")


# Recipe functions #

@app.route('/recipes')
def recipes():
    """
    Lists all recipes in mongoDB data.
    """
    recipes = list(recipes_data.find())
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes/<meal>')
def meals(meal):
    """
    When user clicks on different filter options different
    meal types will display.
    """

    if meal == "breakfast":
        recipes = recipes_data.find({"meal_name": "Breakfast"})
    elif meal == "lunch":
        recipes = recipes_data.find({"meal_name": "Lunch"})
    elif meal == "dinner":
        recipes = recipes_data.find({"meal_name": "Dinner"})
    elif meal == "desserts":
        recipes = recipes_data.find({"meal_name": "Desserts"})

    return render_template(
        'recipes.html', meal=meal, recipes=recipes)


@app.route('/recipes', methods=["GET", "POST"])
def search():
    """
    Searches the recipe index. Will return results for, Recipe name,
    description and ingredients.
    """

    query = request.form.get("search-query")
    recipes = recipes_data.find({"$text": {"$search": query}})

    searched_recipes = recipes.count()

    return render_template("recipes.html", query=query,
                           recipes=recipes, searched_recipes=searched_recipes)


@app.route('/recipe/<recipe_id>')
def recipe_page(recipe_id):
    """
    Returns page for specific recipe ID.
    """

    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)


# Login / register function #

@app.route('/login', methods=["GET", "POST"])
def login():
    """
    If username exists and password is correct user is logged in.
    """

    if request.method == "GET":
        return render_template("login.html")

    session.permanent = True
    password = request.form.get("password")

    existing_user = users_data.find_one(
        {"username": request.form.get("username").lower()})

    if existing_user and check_password_hash(
            existing_user["password"], password):
        session["user"] = request.form.get("username").lower()

        return redirect(url_for(
            "profile", username=session["user"]))

    flash("Incorrect Username and/or Password")
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Checks if username/email is already in use. If not the
    registers Registers new user.
    """

    if request.method == "GET":
        return render_template("register.html")

    existing_username = users_data.find_one(
        {"username": request.form.get("username").lower()})
    existing_email = users_data.find_one(
        {"email": request.form.get("email").lower()})

    if existing_username or existing_email:
        if existing_username:
            flash("Sorry, this username is already in use. Please try another")
        else:
            flash("Sorry, this email is already in use. Please try another")
        return redirect(url_for("register"))

    register = {
        "username": request.form.get("username").lower(),
        "email": request.form.get("email").lower(),
        "password": generate_password_hash(request.form.get("password")),
        "date_joined": date.strftime("%d/%m/%Y"),
        "profile_image": request.form.get(
            "profile_img") or default_pic,
        "saved_recipes": []
    }
    users_data.insert_one(register)

    session["user"] = request.form.get("username").lower()
    flash("Welcome! Thank you for sigining up!😊")
    return redirect(url_for(
        "profile", username=session["user"]))


@app.route('/logout')
@login_required
def logout():
    """
    Logs user out from session.
    """

    flash("Goodbye! You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# User logged in functions #

@app.route('/profile/<username>', methods=["GET", "POST"])
@login_required
def profile(username):
    """
    Profile displays all recipes created by user.
    If admin is logged in they can view all recipes on profile.
    """

    user = users_data.find_one({"username": username})

    if username == "admin":
        recipes = list(recipes_data.find())
    else:
        recipes = list(recipes_data.find(
            {"created_by": session['user']}))

    return render_template(
        "profile.html", user=user, recipes=recipes, username=session['user'])


@app.route('/add-recipe', methods=["GET", "POST"])
@login_required
def add_recipe():
    """
    Add allows user to add their own recipes if logged in.
    """

    if request.method == "GET":
        return render_template('add-recipe.html')

    recipe = {
        "meal_name": request.form.get("meal_name"),
        "recipe_name": request.form.get("recipe_name"),
        "ingredients": request.form.get("ingredients"),
        "description": request.form.get("description").capitalize(),
        "recommendation": request.form.get("recos").capitalize(),
        "yield": request.form.get("yield"),
        "active_time": request.form.get(
            "active_time").replace('mins', 'minutes').title(),
        "total_time": request.form.get(
            "total_time").replace('mins', 'minutes').title(),
        "img_url": request.form.get("img_url"),
        "method": request.form.get("method"),
        "created_by": session["user"],
        "date_created": date.strftime("%d/%m/%Y"),
    }

    recipes_data.insert_one(recipe)
    flash("Recipe Succesfully Added 🍽")
    return redirect(url_for("recipes"))


# Saved Recipe functions #

@app.route('/saved-recipes')
@login_required
def saved_recipes():
    """
    Finds users saved recipes array. Loops through saved
    recipes and assigns recipe to it's ID in recipes data. Adds all
    saved recipe info to list to be returned on page in the template.
    """
    user = users_data.find_one({"username": session["user"]})
    saved = user["saved_recipes"]
    saved_rec = []

    for recipe in saved:
        recipe = recipes_data.find_one({'_id': ObjectId(recipe)})
        saved_rec.append(recipe)

    return render_template(
        'saved-recipes.html', saved=saved, saved_rec=saved_rec)


@app.route('/saved-recipes/save/<recipe_id>', methods=["POST"])
@login_required
def save_recipe(recipe_id):
    """
    Adds recipe to "saved_recipes" array in users data.
    Checks if recipe ID is already in array, If not then push's
    recipe ID to array.
    """
    user = users_data.find_one({"username": session["user"]})
    saved = user["saved_recipes"]

    if request.method == "POST":
        if ObjectId(recipe_id) in saved:
            flash("Recipe already saved!😊")
            return redirect(url_for("recipes"))
        else:
            users_data.update_one(
                user, {"$push": {
                    "saved_recipes": ObjectId(recipe_id)}})

            flash("Recipe Saved to profile!💚")

    return redirect(url_for("recipes"))


@app.route('/saved-recipes/<recipe_id>', methods=["POST"])
@login_required
def remove_saved_recipe(recipe_id):
    """
    Removes recipe ID from the users "saved_recipes" array.
    """
    user = users_data.find_one({"username": session["user"]})

    users_data.update_one(
        user, {"$pull": {"saved_recipes": ObjectId(recipe_id)}})
    flash("Recipe removed from saved")

    return redirect(url_for("saved_recipes"))


# Edit and delete recipes #

@app.route('/edit-recipe/<recipe_id>', methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    """
    Allows the user that has created this recipe or
    the admin to edit any recipe details. Edit's will update
    recipe in recipes data.
    """

    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    created_by = recipes_data.find_one({'created_by': session['user']})

    if request.method == "GET":
        return render_template('edit-recipe.html', recipe=recipe)

    if created_by or session['user'] == "admin":
        recipes_data.update_one(
            {"_id": ObjectId(recipe_id)},
            {'$set': {
                "meal_name": request.form.get("meal_name"),
                "recipe_name": request.form.get("recipe_name"),
                "ingredients": request.form.get("ingredients"),
                "description": request.form.get(
                    "description").capitalize(),
                "recommendation": request.form.get("recos").capitalize(),
                "yield": request.form.get("yield"),
                "active_time": request.form.get(
                    "active_time").replace('mins', 'minutes').title(),
                "total_time": request.form.get(
                    "total_time").replace('mins', 'minutes').title(),
                "img_url": request.form.get("img_url"),
                "method": request.form.get("method"),
                "last_edited_by": session['user']
            }})
        flash("Recipe Updated 😊")
        return redirect(url_for("recipe_page", recipe_id=recipe_id))
    else:
        flash("Not your recipe to edit!")
        return redirect(url_for("recipe_page", recipe_id=recipe_id))


@app.route('/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    """
    Deletes recipe if the user logged in created it or user is admin.
    Checks if recipe ID is in any users "saved_recipes" array,
    if it is then recipe will be deleted from array as well.
    """
    created_by = recipes_data.find_one({'created_by': session['user']})
    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    users_saved = list(users_data.find(
        {"saved_recipes": ObjectId(recipe_id)}))

    if created_by or session['user'] == "admin":
        recipes_data.delete_one(recipe)
        for users in users_saved:
            users_data.update_many(
                users, {"$pull": {"saved_recipes": ObjectId(recipe_id)}})
        flash("Recipe Succesfully Removed!")
    else:
        flash("Not your recipe to delete!")

    return redirect(url_for("recipes"))


# Update / delete user #

@app.route('/delete-account/<username>')
@login_required
def delete_user(username):
    """
    Deletes account if session user is the username that is logged in.
    Recipe will be updated to be managed by admin if user deletes account.
    """

    users_recipes = list(recipes_data.find({"created_by": session["user"]}))

    if username:
        users_data.remove({"username": username})
        session.pop("user")

        for recipe in users_recipes:
            recipes_data.update(
                    recipe,
                    {'$set': {
                        "created_by": "admin"
                    }})

        flash("Sorry to see you go! Your user has been deleted.")
    else:
        flash("This is not your account to delete!")
        return redirect(url_for("profile", username=session['user']))

    return redirect(url_for("login"))


@app.route('/update-password/<username>', methods=["GET", "POST"])
@login_required
def update_password(username):
    """
    Checks current password is the users password.
    Updates password only if the two new passwords match.
    """

    current_password = request.form.get("password")
    new_password = request.form.get('new-password')
    confirm_password = request.form.get("confirm-password")
    users = users_data
    user = users_data.find_one({'username': username})

    if request.method == "GET":
        return render_template(
            'update-password.html', username=session['user'])

    if check_password_hash(user["password"], current_password):
        if new_password == confirm_password:
            users.update_one(
                {'username': username},
                {'$set': {
                    'password': generate_password_hash
                    (new_password)
                }})
            flash("Password updated! 😊")
            return redirect(url_for('profile', username=session['user']))

        flash("Passwords do not match! Please try again😔")
        return redirect(url_for("update_password", username=session['user']))

    flash('Incorrect password. Please try again😔')
    return redirect(url_for('update_password', username=session['user']))


@app.route('/update-profile-pic/<username>', methods=["GET", "POST"])
@login_required
def update_profile_pic(username):
    """
    Updates users profile photo if user is logged in.
    """

    if username:
        users_data.update_one(
            {"username": username},
            {'$set': {
                "profile_image": request.form.get(
                    "profile_img")
            }})

    return redirect(url_for("profile", username=session['user']))


# Newsletter Subscribe #

@app.route('/subscribe', methods=["GET", "POST"])
def subscribe_user():
    """
    Checks if email is subscribed already.
    If email is not subscribed, email is added to database.
    """

    existing_sub = subscribers_data.find_one(
        {"subscriber_email": request.form.get("sub_email")})
    if existing_sub:
        return redirect(request.referrer)
    subscribe = {
        "subscriber_email": request.form.get("sub_email"),
    }
    subscribers_data.insert_one(subscribe)
    return redirect(request.referrer)


# Error Pages #

@app.errorhandler(404)
def page_not_found(error):
    return render_template('/errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('/errors/500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
