# Testing

## Error testing:

### 404: 

If a user tries to access a page that is non existent then they will be directed to the custom 404 page. On this page there is a CTA that redirects the user back to the homepage. I have forced this error by typing a wrong url into the bar. 

![404 Error page](/docs/testing/errors/404-error-page.gif)

### Login & Register Errors: 

If a user tries to login with an incorrect password or username then they will be displayed with a flash error.

![Login error gif](/docs/testing/errors/login-error.gif) 

If a user tried to register with an existing username/email address another flask error will be shown.

![Register error](/docs/testing/errors/register-error.gif) 

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

![WSC Form errors](/docs/testing/eating-vegan-wsc-html-validator-issues.jpg)

- ```type='text'``` Was removed from the textarea field. 
- ```"value=""``` Was added to the select box's to remove the error.

## JSHint

JavaScript code passed through JShint with no major issues. Once run through, it prompted to add some semicolons that were missing. These were all added accordinly.

## Python Testing

Throughout the build process I have debugger=True on in my app.py file, this meant that throughout the build process any errors in my python code would return a server error. I used the jinja prompts to find errors in my code. 

Python code was run through the pep8 validator and code was all right. 
Throughout the building process I checked the problems in the terminal to uncover any PEP8 issues and resolved these as I went. 

![Pep8](/docs/testing/pep8-python-code-check.png)

Pytest is something that I would like to look into in the future for automatic testing. 

## Solutions For Issues Found Whilst Building/Testing:

### User Session Lifetime

During the build of the website I noticed that the session was not ending when a user closed the browser and the user was staying logged in forever. This isn't the best UX as the expected behaviour should be that the user is logged out of the session when closing a browser or after a certain amount of time. In order to fix this I added in the app configuration from flask "PERMANENT_SESSION_LIFETIME" and set the time for this as 120 minutes. This fixed the issue and users will be automatically be logged out of their session after 2 hours. 

### Login Required

Whilst testing/building the website I noticed that if a user was logged out but pressed the back button they would be taken back to the profile page/have access to pages that are only availble to users that are logged in. This isn't the best UX as once a user is logged out, then their session should have ended. In order to fix this I installed the flask-login library and added the 'login_required' function. This function was added to all pages that should only be accessed when a user is logged in. If a user is not logged in then they will be redirected to the login page. 

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

## Form testing:


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

If a user enters an invalid email address for a recipe then the image be a broken link.
  - There is a placeholder image for if a user doesn't provide an image however this does not replace a broken link at the moment. Ideally in the future I would like to implement a way a user can upload their own image directly to the webiste.

If a user has searched for a recipe in the search bar and then presses the back button and then the forward button again then they will be presented by "Confirm Form Resubmission". 

## User Stories Tested:

### New user:

<details><summary>As a new user I would like to be able to register an account.</summary>

![Register Account](/docs/testing/user-story-gifs/register-account.gif)

</details>

<details><summary>As a new user I would like to be able to sign up for the newsletter.</summary>

Add GIF

</details>

<details><summary>As a new user I would like to be able to understand what the website is.</summary>

Add GIF

</details>


### Registered User:

<details><summary>As a user I would like to be able to login to my account.</summary>

![Login gif](/docs/testing/user-story-gifs/login-testing.gif)

</details>


<details><summary>As a user I would like to be able to log out of my account..</summary>

![Logout](/docs/testing/user-story-gifs/logout.gif) 

</details>

<details><summary>As a user I would like to be able to view my profile.</summary>

![View Profile](/docs/testing/user-story-gifs/profile.gif) 

</details>

<details><summary>As a user I would like to be able to create new recipes.</summary>

![Add recipe](/docs/testing/user-story-gifs/add-recipe.gif)

</details>

<details><summary>As a user I would like to be able to view all recipes in one place.</summary>

![View recipes](/docs/testing/user-story-gifs/view-all-recipes.gif)

</details>

<details><summary>As a user I would like to filter through the different meal types.</summary>

![Filter recipes](/docs/testing/user-story-gifs/filter-recipes.gif)

</details>

<details><summary>As a user I would like to be able to search through all recipes.</summary>

![Search Recipe](/docs/testing/user-story-gifs/search.gif)

</details>

<details><summary>As a user I would like to be able to edit recipes that I have created.</summary>

![Edit Recipe](/docs/testing/user-story-gifs/edit-recipe.gif)

#### Changes reflected on recipes page and single recipe page.

![Edit recipe recipe page](/docs/testing/user-story-gifs/edit-recipe-more.gif)

</details>

<details><summary>As a user I would like to be able to remove recipes that I have created.</summary>

ADD GIF WHEN ISSUE FIXED 

</details>

<details><summary>As a user I would like to be able to sign up for the newsletter.</summary>

ADD GIF

</details>

<details><summary>As a user I would like to be able to update my password.</summary>

![Change password tested](/docs/testing/user-story-gifs/password-updated.gif)

#### Logging in with new password: 

![New password tested](/docs/testing/user-story-gifs/updated-password-login.gif)

</details>

<details><summary>As a user I would like to be able to delete my account.</summary>

![Delete user](/docs/testing/user-story-gifs/delete-user.gif)

</details>

<details><summary>As a user I would like to be able to update my profile photo.</summary>

![Change Profile Pic](/docs/testing/user-story-gifs/change-profile-pic.gif)

</details>

