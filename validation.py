from flask import (
    Flask, flash, request, session, redirect, url_for)
from functools import wraps


def login_required(f):
    """
    Decorator to be called on views that require users to be logged in.
    """

    @wraps(f)
    def login_check(*args, **kwargs):
        if 'user' not in session:
            flash("You need to login first!")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return login_check


def password_check(password):
    """
    Code adjusted from
    https://stackoverflow.com/questions/41117733/validation-of-a-password-python.
    This function checks the following:

    If password length is greater than 5 and less than 15
    If password has at least one uppercase letter
    If password has at least one lowercase letter
    If password has at least one number
    If password has any of the required special symbols
    """
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*']

    if len(password) < 5:
        flash('Password must be at least 5 characters.')
        return False
    elif len(password) > 15:
        flash('Password should not exceed 15 characters.')
        return False
    elif not any(char.islower() for char in password):
        flash('Password should have at least one lowercase letter.')
        return False
    elif not any(char.isupper() for char in password):
        flash('Password should have at least one uppercase letter.')
        return False
    elif not any(char.isdigit() for char in password):
        flash('Password should have at least one number.')
        return False
    elif not any(char in symbols for char in password):
        flash('Password should include at least one symbol: !@#$%^&* ')
        return False
    return True


def username_check(username):
    """
    This function checks if username length is greater than 5 and less than 15.
    """
    if len(username) < 5:
        flash('Username must be at least 5 characters.')
        return False
    elif len(username) > 15:
        flash('Username cant be longer than 15 characters.')
        return False
    return True


def valid_registration():
    """
    This function checks both username and password for a valid registration.
    """

    password = request.form.get("password")
    username = request.form.get("username")

    if password_check(password) and username_check(username):
        return True


def valid_recipe():
    """
    This function checks the following:

    That description is no more than 100 characters,
    That recipe name is no longer than 35 characters,
    That recommendations is no longer than 100 characters,
    """

    description = request.form.get("description")
    recipe_name = request.form.get("recipe_name")
    recommendations = request.form.get("recos")

    if len(description) > 100:
        flash("Whoops! 😔 Description can't be longer than 100 characters")
        return False
    elif len(recipe_name) > 35:
        flash("Whoops! 😔 Recipe name can't be longer than 35 characters")
        return False
    elif len(recommendations) > 100:
        flash("Whoops! 😔 Recommendation can't be longer than 100 characters")
        return False
    return True


def valid_password_update():
    """
    This function checks that the two new passwords meet the password criteria
    """

    new_password = request.form.get('new-password')
    confirm_password = request.form.get("confirm-password")

    if password_check(new_password) and password_check(confirm_password):
        return True

