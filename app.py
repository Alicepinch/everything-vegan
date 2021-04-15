import os
from flask import (
    Flask, flash, render_template,
    session, request, url_for, redirect)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_sslify import SSLify
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from validation import (
    valid_registration, login_required, valid_recipe, valid_password_update)
if os.path.exists("env.py"):
    import env


# Config #

app = Flask(__name__)
sslify = SSLify(app)

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
    Displays different meals when different filter options are clicked on page.
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


@app.route('/recipes', methods=["POST"])
def search():
    """
    Searches the recipe index. Will return results for,
    Recipe name, description and ingredients.
    """

    # Fetches users search input
    query = request.form.get("search-query")
    # Search results
    recipes = recipes_data.find({"$text": {"$search": query}})
    # Counts all search results
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
    Logs user in if username exists in database and password is correct.
    """

    # Returns login template
    if request.method == "GET":
        return render_template("login.html")

    session.permanent = True
    password = request.form.get("password")
    existing_user = users_data.find_one(
        {"username": request.form.get("username").lower()})

    # Checks if usersname exists and password matches database
    if existing_user and check_password_hash(
            existing_user["password"], password):
        # Adds user to session
        session["user"] = request.form.get("username").lower()
        return redirect(url_for(
            "profile", username=session["user"]))
    # If the username or password does not exist/match the database
    flash("Incorrect Username and/or Password")
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Registers user and adds to database if the username and email address
    are both new and valid.
    """

    # Returns the register template
    if request.method == "GET":
        return render_template("register.html")

    existing_username = users_data.find_one(
        {"username": request.form.get("username").lower()})
    existing_email = users_data.find_one(
        {"email": request.form.get("email").lower()})
    # Checks username or email isn't already in use
    if existing_username or existing_email:
        if existing_username:
            flash("Sorry, this username is already in use. Please try another")
        else:
            flash("Sorry, this email is already in use. Please try another")
        return redirect(url_for("register"))

    # Checks password and username are correct pattern's from validate.py
    if valid_registration():
        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "date_joined": date.strftime("%d/%m/%Y"),
            "profile_image": request.form.get(
                "profile_img") or default_pic,
            "saved_recipes": []
        }
        # Adds user to users database
        users_data.insert_one(register)
        session["user"] = request.form.get("username").lower()
        flash("Welcome! Thank you for sigining up!😊")
        return redirect(url_for(
            "profile", username=session["user"]))

    return redirect(url_for("register"))


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

@app.route('/profile/<username>')
@login_required
def profile(username):
    """
    Displays all recipes created by user.
    If admin is logged in all recipes will show.
    """

    # Fetches all user's information from database
    user = users_data.find_one({"username": session['user']})

    # Checks if user is admin and returns all recipes
    if session['user'] == "admin":
        recipes = list(recipes_data.find())
    # If user is not admin, users recipes will show
    else:
        recipes = list(recipes_data.find(
            {"created_by": session['user']}))

    return render_template(
        "profile.html", user=user, recipes=recipes, username=session['user'])


@app.route('/add-recipe', methods=["GET", "POST"])
@login_required
def add_recipe():
    """
    Adds new recipe to database if recipe fields are all valid.
    """

    # Returns new recipe template
    if request.method == "GET":
        return render_template('add-recipe.html')

    # Checks all form inputs are correct lengths from validate.py
    if valid_recipe():
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
        # Inserts new recipe to recipes database
        recipes_data.insert_one(recipe)
        flash("Recipe Successfully Added 🍽")
        return redirect(url_for("recipes"))
    # Redirects back to form if invalid recipe
    return redirect(request.referrer)


# Saved Recipe functions #

@app.route('/saved-recipes')
@login_required
def saved_recipes():
    """
    Displays all the users saved recipes array.
    """
    # Fetches users data and their saved recipes
    user = users_data.find_one({"username": session["user"]})
    saved = user["saved_recipes"]
    saved_rec = []  # Creates empty array

    # Loops through users saved recipes
    for recipe_id in saved:
        # Assigns recipe id to it's recipe in data and adds to empty array
        recipe_id = recipes_data.find_one({'_id': ObjectId(recipe_id)})
        saved_rec.append(recipe_id)

    return render_template(
        'saved-recipes.html', saved=saved, saved_rec=saved_rec)


@app.route('/save/<recipe_id>', methods=["POST"])
@login_required
def save_recipe(recipe_id):
    """
    Saves recipe to users saved array if recipe not already saved.
    """
    # Fetches users data and their saved recipes
    user = users_data.find_one({"username": session["user"]})
    saved = user["saved_recipes"]

    # Checks if the recipe is aleady in users saved array
    if ObjectId(recipe_id) in saved:
        flash("Recipe already saved!😊")
        return redirect(request.referrer)
    # If not saved add recipe id to users saved recipe array
    users_data.update_one(
        user, {"$push": {
            "saved_recipes": ObjectId(recipe_id)}})
    flash("Recipe Saved to profile!💚")

    return redirect(request.referrer)


@app.route('/saved-recipes/remove/<recipe_id>', methods=["POST"])
@login_required
def remove_saved_recipe(recipe_id):
    """
    Removes recipe ID from the users "saved_recipes" array.
    """
    # Fetches users data
    user = users_data.find_one({"username": session["user"]})
    # Removes recipe id from users saved recipe array
    users_data.update_one(
        user, {"$pull": {"saved_recipes": ObjectId(recipe_id)}})
    flash("Recipe removed from saved")

    return redirect(request.referrer)


# Edit and delete recipes #

@app.route('/recipe/edit-recipe/<recipe_id>', methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    """
    Allows users to edit a recipe if the user is admin or has created
    the recipe and the edits are all valid.
    Returns 404 if user didn't create recipe or user is not admin to
    avoid other users knowing the URL is correct.
    """

    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    created_by = recipe["created_by"]
    # Checks user logged in is user who created recipe or admin
    if created_by == session['user'] or session['user'] == "admin":
        # Returns edit recipe template
        if request.method == "GET":
            return render_template('edit-recipe.html', recipe=recipe)
        # Checks all form inputs are correct lengths from validate.py
        if valid_recipe():
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
            return redirect(request.referrer)
    # If user didn't create recipe or is not admin, 404 error returns
    else:
        return render_template('/errors/404.html'), 404


@app.route('/recipe/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    """
    Deletes recipe. Checks if recipe ID is in any users "saved_recipes" array,
    if it is then recipe will be deleted from array as well.
    Returns 404 if user didn't create recipe or user is not admin to
    avoid other users knowing the URL is correct.
    """

    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    created_by = recipe["created_by"]
    users_saved = list(users_data.find(
        {"saved_recipes": ObjectId(recipe_id)}))

    # Checks user logged in is user who created recipe or admin
    if created_by == session['user'] or session['user'] == "admin":
        # Loops through all users saved recipes
        for users in users_saved:
            # Removes deleted recipe id from all users saved array
            users_data.update_many(
                users, {"$pull": {"saved_recipes": ObjectId(recipe_id)}})
        recipes_data.delete_one(recipe)
        flash("Recipe Succesfully Removed!")
    # If user didn't create recipe or is not admin, 404 error returns
    else:
        return render_template('/errors/404.html'), 404

    return redirect(url_for("recipes"))


# Update / delete user #

@app.route('/profile/delete-account/<username>')
@login_required
def delete_user(username):
    """
    Deletes users account, recipes created by user will be updated to be
    managed by admin. Returns 404 if the session user is not the username
    passed in the URL to avoid other users knowing the URL is correct.
    """

    users_recipes = list(recipes_data.find({"created_by": session["user"]}))

    # If session user matches username in URL
    if session['user'] == username:
        # Loops through users recipes and updates them to be managed by admin
        for recipe in users_recipes:
            recipes_data.update(
                    recipe,
                    {'$set': {
                        "created_by": "admin"
                    }})
        # Removes user from database
        users_data.remove({"username": session['user']})
        session.pop("user")
        flash("Sorry to see you go! Your user has been deleted.")
    # If session user does not match username, 404 error returns
    else:
        return render_template('/errors/404.html'), 404
    return redirect(url_for("login"))


@app.route('/profile/update-password/<username>', methods=["GET", "POST"])
@login_required
def update_password(username):
    """
    User can update their current password If the current password is correct,
    and that the new passwords match the correct format and match before
    updating password in database.
    """

    current_password = request.form.get("password")
    user = users_data.find_one({'username': session['user']})
    new_password = request.form.get('new-password')
    confirm_password = request.form.get("confirm-password")

    # Returns update password template
    if request.method == "GET":
        return render_template(
            'update-password.html', username=session['user'])

    # Checks current password matches password in database
    if check_password_hash(user["password"], current_password):
        # Checks the new passwords match the password format from validate.py
        if valid_password_update():
            # Checks both new passwords match
            if new_password == confirm_password:
                # Updates the password and redirects to profile page
                users_data.update_one(
                    user,
                    {'$set': {
                        'password': generate_password_hash
                        (new_password)
                    }})
                flash("Password updated! 😊")
                return redirect(url_for('profile', username=session['user']))
            else:
                flash("Passwords do not match! Please try again😔")
                return redirect(url_for("update_password",
                                        username=session['user']))
        return redirect(url_for('update_password', username=session['user']))
    else:
        flash('Incorrect password. Please try again😔')
        return redirect(url_for('update_password', username=session['user']))


@app.route('/profile/update-profile-pic', methods=["POST"])
@login_required
def update_profile_pic():
    """
    Updates users profile photo if user is logged in.
    """

    users_data.update_one(
        {"username": session['user']},
        {'$set': {
            "profile_image": request.form.get(
                "profile_img")
        }})
    return redirect(request.referrer)


# Newsletter Subscribe #

@app.route('/subscribe', methods=["POST"])
def subscribe_user():
    """
    Subscribes email to newsletter if email is not subscribed already.
    """

    existing_sub = subscribers_data.find_one(
        {"subscriber_email": request.form.get("sub_email")})
    if not existing_sub:
        subscribe = {
            "subscriber_email": request.form.get("sub_email")}
        subscribers_data.insert_one(subscribe)
    return redirect(request.referrer)


# Error Pages #

@app.errorhandler(404)
def page_not_found(error):
    '''
    Handles 404 error (page not found)
    '''
    return render_template('/errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    '''
    Handles 500 error (internal server error)
    '''
    return render_template('/errors/500.html'), 500


@app.errorhandler(405)
def method_not_allowed(error):
    '''
    Handles 405 error (method not allowed)
    '''
    return render_template('/errors/405.html'), 405


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
