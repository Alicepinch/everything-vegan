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


# Pages #

default_img = ("/static/images/default-recipe-image.jpg")
default_reco = "No Recommendations for this recipe"
default_pic = ("/static/images/default-profile-picture.jpg")
date = date.today()


def login_required(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
            flash("You need to login first")
        else:
            return f(*args, **kwargs)
    return login_check


# Homepage #


@app.route('/')
def index():
    return render_template("index.html")


# Recipe functions #

@app.route('/recipes/<meal_name>')
def meals(meal_name):
    meal_name = mongo.db.recipes.find({"meal_name": meal_name})
    if meal_name == "Breakfast":
        mongo.db.recipes.find({meal_name['Breakfast']})
    elif meal_name == "Lunch":
        mongo.db.recipes.find({meal_name['Lunch']})
    elif meal_name == "Dinner":
        mongo.db.recipes.find({meal_name['Dinner']})
    elif meal_name == "Dessert":
        mongo.db.recipes.find({meal_name['Dessert']})

    return render_template('recipes.html', meal_name=meal_name)


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
    If not results match - flash message
    will show.
    """
    query = request.form.get("search-query")
    all_recipes = mongo.db.recipes.find().count()
    recipes = mongo.db.recipes.find({"$text": {"$search": query}})

    if all_recipes > 0:
        return render_template("recipes.html", recipes=recipes)
    else:
        flash("Sorry! No results found 😔")
        return render_template("recipes.html", recipes=recipes)


@app.route('/recipe/<recipe_id>')
def recipe_page(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)


# Login / register function #


@app.route('/login', methods=["GET", "POST"])
def login():
    session.permanent = True
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
        if existing_username:
            flash("Sorry, this username already exists. Please try another")
            return redirect(url_for("register"))

        # Finds the email in the mongo DB database.
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})
        if existing_email:
            flash("Sorry, this email is in use. Please try another")
            return redirect(url_for("register"))

        # Inserts register dict to data if username & email is new.
        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "date_joined": date.strftime("%d/%m/%Y"),
            "profile_image": request.form.get(
                                 "profile_img") or default_pic
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Welcome! Thank you for sigining up!😊")
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
    user = mongo.db.users.find_one({"username": session['user']})

    if session['user'] == "admin":
        recipes = list(mongo.db.recipes.find())
    else:
        recipes = list(mongo.db.recipes.find(
                {"created_by": session['user']}))
    return render_template(
        "profile.html", user=user, recipes=recipes, username=username)


@app.route('/add-recipe', methods=["GET", "POST"])
@login_required
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
            "recommendation": request.form.get("recos") or default_reco,
            "yield": request.form.get("yield"),
            "active_time": request.form.get("active_time"),
            "total_time": request.form.get("total_time"),
            "img_url": request.form.get("img_url") or default_img,
            "method": request.form.get("method"),
            "created_by": session["user"],
            "date_created": date.strftime("%d/%m/%Y")
        }

        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Succesfully Added")
        return redirect(url_for("recipes"))

    return render_template('add-recipe.html')


@app.route('/edit-recipe/<recipe_id>', methods=["GET", "POST"])
@login_required
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
                "recommendation": request.form.get("recos") or default_reco,
                "yield": request.form.get("yield"),
                "active_time": request.form.get("active_time"),
                "total_time": request.form.get("total_time"),
                "img_url": request.form.get("img_url"),
                "method": request.form.get("method") or default_img,
                "created_by": session["user"]
            }})

        flash("Recipe Updated 😊")
        return redirect(url_for("recipes"))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('edit-recipe.html', recipe=recipe)


@app.route('/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    """
    Removes recipe from database and recipes page.
    """
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Succesfully Removed!")
    return redirect(url_for("recipes"))


# Update/ delete users #


@app.route('/delete-account/<username>')
@login_required
def delete_user(username):
    """
    Ends user session.
    Removes user & all
    recipes created by user.
    """
    mongo.db.users.remove({"username": session['user']})
    session.pop("user")
    mongo.db.recipes.remove({"created_by": session['user']})

    flash("Sorry to see you go! Your user has been deleted.")
    return redirect(url_for("login"))


@app.route('/update-user/<username>', methods=["GET", "POST"])
@login_required
def update_user(username):

    current_password = request.form.get("password")
    new_password = request.form.get('new-password')
    confirm_password = request.form.get("confirm-password")
    users = mongo.db.users
    user = mongo.db.users.find_one({'username': session['user']})

    if request.method == "POST":

        if check_password_hash(user["password"], current_password):

            if new_password == confirm_password:
                users.update_one(
                    {'username': session['user']},
                    {'$set': {
                        'password': generate_password_hash
                        (new_password)
                    }})
                flash("Password has been updated!")
                return redirect(url_for('profile', username=username))

            else:
                flash("New passwords do not match! Please try again")
                return redirect(url_for("update_user", username=username))
        else:
            flash('Incorrect original password. Please try again')
            return redirect(url_for('update_user', username=username))

    return render_template('update-user.html', username=username)


@app.route('/update-profile-pic/<username>', methods=["GET", "POST"])
@login_required
def update_profile_pic(username):
    """
    Updates users profile photo.
    """
    mongo.db.users.update_one(
        {"username": session['user']},
        {'$set': {
            "profile_image": request.form.get(
                                 "profile_img") or default_pic
            }})
    return redirect(url_for("profile", username=username))


# Newsletter Subscribe #


@ app.route('/subscribe', methods=["GET", "POST"])
def subscribe_user():
    """
    First checks if email is subscribed already.
    If email is not subscribed, email is added to database.
    """
    existing_sub = mongo.db.subscribers.find_one(
            {"subscriber_email": request.form.get("sub_email")})

    if existing_sub:
        flash("Already Subscribed!")
        return redirect(request.referrer + "#subscription-container")

    subscribe = {
        "subscriber_email": request.form.get("sub_email"),
        }
    mongo.db.subscribers.insert_one(subscribe)
    flash("Thank you for subscribing!")
    return redirect(request.referrer + #subscription-container)


# Error Pages #

@ app.errorhandler(404)
def page_not_found(error):
    return render_template('/errors/404.html'), 404


@ app.errorhandler(500)
def internal_server_error(error):
    return render_template('/errors/500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
