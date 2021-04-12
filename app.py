import os
from flask import (
    Flask, flash, render_template,
    session, request, url_for, redirect)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from validation import (valid_registration,
    login_required, valid_recipe, valid_password_update)
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


@app.route('/recipes', methods=["POST"])
def search():
    """
    This function searches the recipe index. Will return results for,
    Recipe name, description and ingredients.
    If no recipes for query searched, jinja templating
    returns "No results found".
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
    This function does the following:

    Checks if the username or email is already in the users database,
    If they are user cannot register.
    If not and registration fields are valid then user is registered and
    added to database.
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

    # Checks password and username are correct pattern from validate.py
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
    This function displays all recipes created by user.
    If admin is logged in all recipes are displayed.
    """
    user = users_data.find_one({"username": username})

    if username == "admin":
        recipes = list(recipes_data.find())
    else:
        recipes = list(recipes_data.find(
            {"created_by": username}))

    return render_template(
        "profile.html", user=user, recipes=recipes, username=session['user'])


@app.route('/add-recipe', methods=["GET", "POST"])
@login_required
def add_recipe():
    """
    This function checks if the recipe fields are valid then pushes
    all the data to the recipes data.
    """

    if request.method == "GET":
        return render_template('add-recipe.html')

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

        recipes_data.insert_one(recipe)
        flash("Recipe Succesfully Added 🍽")
        return redirect(url_for("recipes"))

    return redirect(request.referrer)


# Saved Recipe functions #

@app.route('/saved-recipes')
@login_required
def saved_recipes():
    """
    This function does the following:

    Finds the users saved recipes arry.
    Loops through all the saved recipes.
    Finds the saved recipe ID in the recipes data.
    Adds the recipe a seperate array to be returns on the page in template.
    """
    user = users_data.find_one({"username": session["user"]})
    saved = user["saved_recipes"]
    saved_rec = []

    for recipe_id in saved:
        recipe_id = recipes_data.find_one({'_id': ObjectId(recipe_id)})
        saved_rec.append(recipe_id)

    return render_template(
        'saved-recipes.html', saved=saved, saved_rec=saved_rec)


@app.route('/save/<recipe_id>', methods=["POST"])
@login_required
def save_recipe(recipe_id):
    """
    This function does the follow:

    Checks if recipe_id is in users saved_recipes array
    If recipe_id in saved array then recipe is not saved
    If recipe_id is not in saved, recipe_id is pushed to array.
    """
    user = users_data.find_one({"username": session["user"]})
    saved = user["saved_recipes"]

    if ObjectId(recipe_id) in saved:
        flash("Recipe already saved!😊")
        return redirect(request.referrer)

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
    user = users_data.find_one({"username": session["user"]})

    users_data.update_one(
        user, {"$pull": {"saved_recipes": ObjectId(recipe_id)}})
    flash("Recipe removed from saved")

    return redirect(request.referrer)


# Edit and delete recipes #

@app.route('/recipe/edit-recipe/<recipe_id>', methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    """
    This function allows allows users to edit a recipe.

    If the user has created the recipe or is the admin,
    If the edits are all valid.
    """
    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    created_by = recipe["created_by"]
    user = users_data.find_one({'username': session['user']})

    if created_by == user or user == "admin":
        if request.method == "GET":
            return render_template('edit-recipe.html', recipe=recipe)
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
    else:
        return render_template('/errors/500.html'), 500


@app.route('/recipe/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    """
    Deletes recipe if the user logged in created it or user is admin.
    Checks if recipe ID is in any users "saved_recipes" array,
    if it is then recipe will be deleted from array as well.
    """
    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})
    created_by = recipe["created_by"]
    users_saved = list(users_data.find(
        {"saved_recipes": ObjectId(recipe_id)}))
    user = users_data.find_one({'username': session['user']})

    if created_by == user or user == "admin":
        for users in users_saved:
            users_data.update_many(
                users, {"$pull": {"saved_recipes": ObjectId(recipe_id)}})
        recipes_data.delete_one(recipe)
        flash("Recipe Succesfully Removed!")
    else:
        return render_template('/errors/500.html'), 500

    return redirect(url_for("recipes"))


# Update / delete user #

@app.route('/profile/delete-account/<username>')
@login_required
def delete_user(username):
    """
    Deletes account if session user is the username that is logged in.
    Recipe will be updated to be managed by admin if user deletes account.
    """

    users_recipes = list(recipes_data.find({"created_by": session["user"]}))

    if session['user'] == username:
        for recipe in users_recipes:
            recipes_data.update(
                    recipe,
                    {'$set': {
                        "created_by": "admin"
                    }})
        users_data.remove({"username": username})
        session.pop("user")
        flash("Sorry to see you go! Your user has been deleted.")
    else:
        return render_template('/errors/500.html'), 500
    return redirect(url_for("login"))


@app.route('/profile/update-password/<username>', methods=["GET", "POST"])
@login_required
def update_password(username):
    """
    This function checks the following:

    If current password matches the users password,
    If the two new passwords are valid passwords
    If the two new passwords match
    If all the above are true, password is updated
    """

    current_password = request.form.get("password")
    user = users_data.find_one({'username': username})
    new_password = request.form.get('new-password')
    confirm_password = request.form.get("confirm-password")

    if request.method == "GET":
        return render_template(
            'update-password.html', username=session['user'])

    if check_password_hash(user["password"], current_password):
        if valid_password_update():
            if new_password == confirm_password:
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


@app.route('/profile/update-profile-pic/<username>', methods=["POST"])
@login_required
def update_profile_pic(username):
    """
    Updates users profile photo if user is logged in.
    """

    if session['user'] == username:
        users_data.update_one(
            {"username": username},
            {'$set': {
                "profile_image": request.form.get(
                    "profile_img")
            }})
    return redirect(url_for("profile", username=session['user']))

# Newsletter Subscribe #


@app.route('/subscribe', methods=["POST"])
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


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('/errors/405.html'), 405


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
