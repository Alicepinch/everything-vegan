# Testing

### 404 & 500: 

If a user tries to access a page that is non existent then they will be directed to the custom 404 page. On this page there is a CTA that redirects the user back to the homepage. I have forced this error by typing a wrong url into the bar. 

In case of an internal server error occuring then a 500 error page has also been implemented. This looks similar to the 400 error page and has a CTA for users to click back to the homepage. 

![404 Error page](/docs/testing/errors/404-error-page.gif)

## Lighthouse Reports:

<details><summary>Homepage</summary>

![Homepage lighthouse report](/docs/testing/lighthouse-reports/homepage-lighthouse-report.png)

</details>

<details><summary>Recipes Page & Single Recipe Page</summary>

![Recipes page lighthouse report](/docs/testing/lighthouse-reports/recipes-lighthouse-report.png)
![Recipe page lighthouse report](/docs/testing/lighthouse-reports/recipe-page-lighthouse-report.png)

</details>

<details><summary>Login & Register Pages</summary>

![Login lighthouse report](/docs/testing/lighthouse-reports/login-lighthouse-report.png)
![Register lighthouse report](/docs/testing/lighthouse-reports/register-lighthouse-report.png)

</details>

<details><summary>New Recipe & Edit Recipe</summary>

![New Recipe lighthouse report](/docs/testing/lighthouse-reports/add-recipe-lighthouse-report.png)
![Edit Recipe lighthouse report](/docs/testing/lighthouse-reports/edit-recipe-lighthouse-report.png)

</details>

<details><summary>Profile Page</summary>

![Profile lighthouse report](/docs/testing/lighthouse-reports/profile-lighthouse-report.png)

</details>

## WSC Validator:

CSS Validator returned no errors.
![WSC CSS Validator](/docs/testing/eating-vegan-wsc-css-validator.jpg)

HTML Validator returned errors for Jinja templating which is expected behaviour. Some issues were raised for both the 'edit-recipe.html" and "add-recipe.html" forms as below. No other issues were found when running HTML through the validator.

![WSC errors](/docs/testing/eating-vegan-wsc-html-validator-issues.jpg)

- ```type='text'``` Was removed from the textarea field. 
- ```"value=""``` Was added to the select box's to remove the error.

## JSHint

JavaScript code passed through JShint with no major issues. Once run through, it prompted to add some semicolons that were missing. These were all added.

## Python Testing

Throughout the build process I have debugger=True on in my app.py file, this meant that throughout the build process any errors in my python code would return a server error. I used the jinja prompts to find errors in my code. 

Python code was run through the pep8 validator and code was all right. 
Throughout the building process I checked the problems in the terminal to uncover any PEP8 issues and resolved these as I went. 

![Pep8](/docs/testing/pep8-python-code-check.png)

Pytest is something that I would like to look into in the future for automatic testing. 

## Solutions For Issues Found Whilst Building/Testing:

### User Session Lifetime

During the build I noticed that the session was not ending when a user closed the browser and the user was staying logged in forever. This isn't the best UX as the expected behaviour should be that the user is logged out of the session when closing a browser or after a certain amount of time. In order to fix, I added in the app configuration from flask "PERMANENT_SESSION_LIFETIME" and set the time for this as 120 minutes. This fixed the issue and users will be automatically be logged out of their session after 2 hours. 

### Login Required

Whilst testing/building the website I noticed that if a user was logged out but pressed back they would be taken back to the profile page/have access to pages that are for users that are logged in. This isn't the best UX as once a user is logged out, then their session should have ended. In order to fix, I installed the flask-login library and added the 'login_required' function. This function was added to all pages that should only be accessed when a user is logged in. If a user is not logged in then they will be redirected to the login page. 

Code added:
```
def login_required(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)
    return login_check
```

### Saved recipes:

When testing the save recipe function I noticed that if a user had saved a recipe that had been deleted by another user, it was still in their "saved_recipe" array in mongodb. This wasnt ideal as the recipe didn't exist anymore. However, was still displaying on their saved recipes page. In order to fix this I needed to loop through all the users in mongoDB and then loop through all of the users "saved_recipes" arrays in order to check whether the recipe being deleted was in there. If it was then this needed to be deleted. The below code was the solution for this.

Code Before:

```
@app.route('/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    created_by = recipes_data.find_one({'created_by': session['user']})
    recipe = recipes_data.find_one({"_id": ObjectId(recipe_id)})

    if created_by or session['user'] == "admin":
        recipes_data.delete_one(recipe)
        flash("Recipe Succesfully Removed!")
    else:
        flash("Not your recipe to delete!")

    return redirect(url_for("recipes"))

```

Code after:

```
@app.route('/delete-recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
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

```

### Deleting account & Recipes:

When doing my final tests, I noticed that if anyone was logged in they were able to delete any account/recipes. Even though the button for 'delete recipe' and 'delete account' only showed to users that created that specific recipe/ on their profile. If someone was to just use the url ```delete-recipe/<recipe-id>``` or ```delete-user/<username>```  then they would be able to override the Jinja templating. This wasn't ideal as I wouldn't want any user to be able to delete any recipe/account just because they are logged in. To remedy this, I added in some if statements to the appropriate routes in my [app.py](app.py) file to ensure that the person deleting recipe was either the user that created it or the admin. If the users is neither of these then they will be told that they cannot perform these actions.

## Form Testing:

All required form fields have been marked with an '*' and this has been stated either above the form or below excluding the login form. 

#### Register Form:

Register form has been tested by filling out each required form field and submitting. Once form is submitted user details are pushed to the users collection in mongoDB databse. 
  - Form fields that are required: Email address, username and password. Profile photo is not required and if used doesn't fill this in a default profile picture will be used.

If a user tried to register with an existing username/email address a flash error message will be shown and users not registered.

![Register error](/docs/testing/errors/register-error.gif) 

#### Login form:

Login form has been tested by using the same details that were used to register. Once form is submitted user is succesfully logged in and directed to profile page. 
  - Password and Username are both required fields and a user cannot log in without either or. 

If a user tries to login with an incorrect password or username then they will be displayed with a flash error message and user is not logged in.

![Login error gif](/docs/testing/errors/login-error.gif) 

#### Subscribe Newsletter:

User can enter their email address to subscribe to newsletter by clicking 'Subscribe' button, once submitted email address is saved in subscribers collection in mongoDB.

#### Add Recipe:

The Add Recipe form has been tested by adding numerous recipes to the website. Each form field was filled out one by one and submitted after each one to test that the the correct form fields were required. All form fields are required for the Add Recipe form except from "Recommendation" and "Image". If "Recommendation" is left empty then on the recipe page this section is hidden. If the "Image" field is left blank then Jinja templating will display a default recipe image. 
  - Once submitted all the recipes data is succesfully pushed and saved in the mongoDB recipes collection.

#### Edit Recipe:

The edit recipe form has been tested in the same way as the "Add recipe" form. However, when testing this form I noticed that if a user hadn't entered a image url and the default image was being used "/static/images/default-recipe-image.jpg" then a user could not submit the edit form as the form field pattern for this was ```pattern="https://.*"``` and input field was "url". In order to fix this, I added in jinja templating to add the default recipe image rather than have this in the form field itself. 
  - Once the edit form is submitted the recipes data is succesfully updated in the mongoDB recipes collection.


#### Search:

The search function form has been tested, users are able to search by recipe name, description as well as ingreditents. If the query that they search does not exist then a "No results for "query"" message displays to the users. When testing the search function I came across the error "Confirm Form Submission" if a user had clicked on a searched recipe and then back to the recipe page. In order to fix this I used the below code in my JS file:

```

if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

````

[Search no results found](/docs/testing/search-no-results-found.png)

## Usability Testing:

This website has been cross checked on the below devices and browsers to test responsiveness:

iPhone 11 Plus
- Safari
- Chrome

MacBook Pro 13"
 - Safari
 - Chrome
 - Firefox
 - Microsoft Edge

iMac
 - Safari
 - Chrome
 - Firefox
 - Microsoft Edge


## Known Errors: 

When testing on safari I found an issue with the select drop down css didn't apply on the forms. I have not corrected this as prioritised other issues for now. 

If a user enters an invalid image url for a recipe then the image be a broken link.
  - There is a placeholder image for if a user doesn't provide an image however this does not replace a broken link at the moment. Ideally in the future I would like to implement a way a user can upload their own image directly to a cloud.

## User Stories Tested:

### New user:

<details><summary>As a new user I would like to be able to register an account.</summary>

<br>
When a user enters the site, they can navigate to the 'Register' link in the navbar or the CTA in the promotional section below the header to register an account with eating vegan. 

![Register Account](/docs/testing/user-story-gifs/register-account.gif)

</details>

<details><summary>As a new user I would like to be able to sign up for the newsletter.</summary>

<br>
On any page of the website a user can scroll to the bottom of any page and fill in their email address to subscribe to the newsletter.

</details>

<details><summary>As a new user I would like to be able to understand what the website is.</summary>

<br>
When a user lands on the homepage of the website they will be provided with content about the website and what it is. They can also explore the 'Recipes' page in the navbar to get an idea of what is shared on the website.

</details>


### Registered User:

<details><summary>As a user I would like to be able to login to my account.</summary>

<br>
When a user enters the site, they can navigate to the 'Login' link in the navbar to login to their account where they will fill in their login details. Once they have entered their details they will be directed to their profile page.

![Login gif](/docs/testing/user-story-gifs/login-testing.gif)

</details>

<details><summary>As a user I would like to be able to log out of my account.</summary>

<br>
When a user is logged into their account a 'Logout' navigation link will appear that users can click to end their session. 

![Logout](/docs/testing/user-story-gifs/logout.gif) 

</details>

<details><summary>As a user I would like to be able to view my profile.</summary>

<br>
When a user is logged into their account they will have a 'Profile' link in the navigation bar that they can click to view their profile. 

![View Profile](/docs/testing/user-story-gifs/profile.gif) 

</details>

<details><summary>As a user I would like to be able to create new recipes.</summary>

<br>
When a user is logged into their account they will have a 'New Recipe' link in the navigation bar that they can click. This will lead them to a form where they can enter in all the details of their new recipe and submit it. 

![Add recipe](/docs/testing/user-story-gifs/add-recipe.gif)

</details>

<details><summary>As a user I would like to be able to view all recipes in one place.</summary>

<br>
A user can view all recipes by clicking the 'Recipes' link in the navigation bar. 

![View recipes](/docs/testing/user-story-gifs/view-all-recipes.gif)

</details>

<details><summary>As a user I would like to filter through the different meal types.</summary>

<br>
When a user is on the 'Recipes' page a user can click on the filter button. This will open a drop down menu of the different meal types where a user can click through to display 'Lunch' 'Dinner' 'Breakfasts' and 'Desserts' they also have the option to view all recipes again.

![Filter recipes](/docs/testing/user-story-gifs/filter-recipes.gif)

</details>

<details><summary>As a user I would like to be able to search through all recipes.</summary>

<br>
When a user is on the 'Recipes' page there is a search bar at the top. Users are able to search for key words which will be in the recicpes Name, description or ingredients. They can also reset the search bar to display all recipes again.

![Search Recipe](/docs/testing/user-story-gifs/search.gif)

</details>

<details><summary>As a user I would like to be able to edit recipes that I have created.</summary>

<br>
Once a user has created a recipe, this will be displayed on their profile page. The user can click the 'Edit Recipe' CTA on any of the recipes they have created. They will be lead to a prefilled form with all the content they had previously entered where they can edit accordingly.

![Edit recipe](/docs/testing/user-story-gifs/edit-recipe.gif)

</details>

<details><summary>As a user I would like to be able to remove recipes that I have created.</summary>

<br>
To delete a recipe a user must either go to the recipe page and click on the 'Delete Recipe' CTA at the bottom of the page, or on the edit page. This will only be displayed if the user has created the recipe or the user logged in is the admin. 

![Delete recipe edit page](/docs/testing/user-story-gifs/delete-recipe-edit-page.gif)

![Delete recipe recipe page](/docs/testing/user-story-gifs/delete-recipe-recipe-page.gif)

</details>

<details><summary>As a user I would like to be able to sign up for the newsletter.</summary>

<br>
On any page of the website a user can scroll to the bottom of any page and fill in their email address to subscribe to the newsletter.

</details>

<details><summary>As a user I would like to be able to update my password.</summary>

<br>
A user is able to update their password on their profile page. They can click on the "Update password" CTA under their profile picture. This leads them to a form where they need to confirm their current password in order to update it.

![Change password tested](/docs/testing/user-story-gifs/password-updated.gif)

#### Logging in with new password: 

![New password tested](/docs/testing/user-story-gifs/updated-password-login.gif)

</details>

<details><summary>As a user I would like to be able to delete my account.</summary>

<br>
A user is able to delete their profile from their profile page. Underneath their profile photo is a "Delete profile" CTA. Users will be promted to confirm deletion before this action is completed. 

![Delete user](/docs/testing/user-story-gifs/delete-user.gif)

</details>

<details><summary>As a user I would like to be able to update my profile photo.</summary>

<br>
A user is able to update their profile photo on their profile page. Underneath the photo is an 'Update Profile' CTA where they can add a new photo url to be used as thier profile photo. 

![Change Profile Pic](/docs/testing/user-story-gifs/change-profile-pic.gif)

</details>

<details><summary>As a user I would like to be able to save recipes to my profile.</summary>

<br>
A user is able to save their recipe to their "saved_recipes" array in mongoDB and access all saved recipes from their profile.

![Save Recipe](/docs/testing/user-story-gifs/save-recipe.gif)

</details>

<details><summary>As a user I would like to be able to remove save recipes.</summary>

<br>
A user can remove any recipes from their saved by clicking on the "remove saved recipe" on the saved recipes page. 

![Remove Saved Recipe](/docs/testing/user-story-gifs/remove-saved-recipe.gif)

</details>