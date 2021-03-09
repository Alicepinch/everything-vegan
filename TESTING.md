# Testing

#### User Session Lifetime:

During the build of the website I noticed that the session was not ending when a user closed the browser and the user was staying logged in forever. This isn't the best UX as the expected behaviour should be that the user is logged out of the session when closing a browser or after a certain amount of time. In order to fix this I added in the app configuration from flask "PERMANENT_SESSION_LIFETIME" and set the time for this as 120 minutes. This fixed the issue and users will be automatically be logged out of their session after 2 hours. 

### Login Required:

Whilst testing/building the website I noticed that if a user was logged out but pressed the back button they would be taken back to the profile page/ have access to pages that are only availble to users that are logged in. This isn't the best UX as once a user is logged out, then their session should have ended. In order to fix this I installed the flask-login library and added the 'login_required' function. This function was added to all pages that should only be accessed when a user is logged in. If a user is not logged in then they will be redirected to the login page. 

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

### Deleting Recipe's:

When testing the delete function for the recipes on the profile I noticed that when trying to delete a recipe from the bottom of the page it was deleting the first recipe instead of the selected one. To fix this I....

### Lighthouse:
---


### WSC Validator:
---

CSS Validator returned no errors.
![WSC CSS Validator](/docs/testing/eating-vegan-wsc-css-validator.jpg)

HTML Validator returned errors for Jinja templating which is expected behaviour. Some issues were raised for both the 'edit-recipe.html" and "add-recipe.html" forms as below. No other issues were found when running HTML through the validator.

![WSC Form errors](/docs/testing/eating-vegan-wsc-html-validator-issues.jpg)

- ```type='text'``` Was removed from the textarea field. 
- ```"value=""``` Was added to the select box's to remove the error.

### JSHint
---

JavaScript code passed through JShint with no major issues. Once run through it prompted to add some semicolons that were missing. These were all added accordinly.

### Usability Testing:
---

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

When testing on safari there is a known design issue. 
On the forms when a user is logged in, the select box is not styled the same as in Chrome, Firefox and Edge. 


### User Stories Tested:
---

<details><summary>New User</summary>
<p>

As a user I would like to be able to login to my account.
![Login gif](/docs/testing/login-testing.gif)
As a user I would like to be prompted if my password is incorrect.
![Login error gif](/docs/testing/login-testing.gif) 
As a user I would like to be able to log out of my account.
![Logout](/docs/testing/logout.gif) 
As a user I would like to be able to view my profile.
![View Profile](/docs/testing/profile.gif) 
As a user I would like to be able to edit or remove recipes that I have created.
![Edit Recipe](/docs/testing/edit-recipe.gif)
![Edit recipe recipe page]()
- As a user I would like to be able to view all recipes in one place.
- As a user I would like to be able to create new recipes.
- As a user I would like to be able to sign up for the newsletter.
- As a user I would like to be able to update my account details.
- As a user I would like to be able to delete my account.
- As a user I would like to flick through the different meal types.
- As a user I would like to be able to search through all recipes.
- As a user I dont want to have all naviagtion links when not applicable.

</p>

</details>

<details><summary>Returning User</summary>
<p>

- As a new user I would like to be able to register an account.
- As a new user I would like to be able to sign up for the newsletter.
- As a new user I would like to be able to understand what the website is.
- As a new user 

</details>

<details><summary>Admin</summary>
<p>

- As an admin I would like to be able to edit any recipe.
- As an admin I would like the option to delete any recipes incase they don't meet the guidelines.
- As an admin I would like to be able to delete users if needed. 
</p>

</details>

