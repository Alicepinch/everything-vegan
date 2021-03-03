# Eating Vegan

“Eating Vegan” is an online community where users can create and explore new exclusively vegan recipes with each other. Users of "Eating Vegan" will have the option to create an account where they will be able to login to create, read, update and delete Vegan recipes. 
 
## UX

The UX goal of this website is...

<details><summary>Strategy</summary>
<p>

#### User stories:

- As a user I would like to be able to login to my account.
- As a user I would like to be able to log out of my account.
- As a user I would like to be able to view my profile.
- As a user I would like to be able to edit or remove recipes that I have created.
- As a user I would like to be able to view all recipes in one place.
- As a user I would like to be able to create new recipes.
- As a user I would like to be able to sign up for the newsletter.
- As a user I would like to be able to update my account details.
- As a user I would like to be able to delete my account.
- As a user I would like to flick through the different meal types.
- As a user I would like to be able to search through all recipes.
- As a user I dont want to have all naviagtion links when not applicable.

#### Returning User:

- As a new user I would like to be able to register an account.
- As a new user I would like to be able to sign up for the newsletter.
- As a new user I would like to be able to understand what the website is.
- As a new user 

#### Admin:

- As an admin I would like to be able to edit any recipe.
- As an admin I would like the option to delete any recipes incase they don't meet the guidelines.
- As an admin I would like to be able to delete users if needed. 
</p>

</details>

<details><summary>Scope</summary>
<p>

#### Planned features:

</p>
</details>

<details><summary>Structure</summary>
<p>



</p>
</details>

<details><summary>Skeleton</summary>
<p>

[User Logged In Wireframes](/docs/eating-vegan-wireframe-logged-in.png)

[User Logged Out Wireframes](/docs/eating-vegan-wireframe-logged-out.png)

</p>
</details>
<details><summary>Surface</summary>
<p>

#### Design:


#### Typography:

Font's I have chosen for this project are 'Bungee Shade', 'Bungee' and 'Roboto'. The reason I have chosen these fonts is because I wanted the design of 'Eating Vegan' to be eye catching and I found the Bungee font's stood out from any others. Bungee Shade will be used for all page headings. Bungee for all subheadings throughout and Roboto will be used for all links, p elements and buttons.

#### Colour Scheme


</p>
</details>

## Data schema:

### MongoDB

- The database used for this project is an NoSQL database. The database was created using the MongoDB cross-platform document-oriented program.

### Data types

- The datatypes that have been used in this project are:
    - ObjectId
    - String
    
### Collections in database:

For this project I created a database in MongoDB called vegan_cookbook. Inside of this database I created 4 different collections to be used for this website.

- Users
- Recipes
- Subscribers 
- Meals

#### Views

- A view will begin at 1 when the recipe has been created & will then increment by 1 every time that a
recipe is used on the website with the corresponding ID.

## Features Implemented
 
- [x] Login
- [x] Register
- [x] Profile Page
- [x] Recipe Page
- [x] Edit Recipe
- [x] Add new recipe
- [x] Update user information
- [x] Newsletter Subscription
- [x] Flash messages
- [x] Search recipes
- [x] If a user is logged out and tries to access any 'login_required' pages they will be redirected to login page.
- [x] Single recipe page.
- [x] 404 page.
- [x] 505 page.
- [x] Update user information.
- [x] Delete account.

### Features Left to Implement

- [ ] Page Pagination.
- [ ] User profiles with option to upload images.
- [ ] Automated email when user signs up.
- [ ] User could upload an image.
- [ ] Option to view other users and what they have uploaded.
- [ ] More specific filters for recipes.
 
## Technologies Used

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- Python 3.8.2
    * Flask
    * Jinja 
    * Werkzeug security
- Flask
- MongoDB
- HTML
- CSS
- Heroku
- Bootstrap
- Git & GitHub.com

### Other Tools Used

- [Font Awesome](https://fontawesome.com/) 
- [Google fonts](https://fonts.google.com/) 
- [Balsamiq](https://balsamiq.com/) 
- [Gimp](https://www.gimp.org/) 
- [W3Schools](https://www.w3schools.com/) 
- [StackOverflow](https://stackoverflow.com/) 
- [Coloors](https://coolors.co/) 
- [Favicon generator](https://www.favicon-generator.org/) 
- [JShint](https://jshint.com/) 
- [W3cValidator](https://validator.w3.org/)
- Google chrome developer tools.
- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
  - [Flask error pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages)
  - [For view decorators](https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/)
  - [For permanent session cookie](https://flask.palletsprojects.com/en/1.1.x/config/)

## Testing

All the testing carried out for Eating Vegan can be found [here](TESTING.md)

## Deployment

In order to run this on your local IDE you need to insure you have the following installed on your machine:

- PIP
- Python
- Git
- You will also need an account on MongoDB 

### Creating a local repository 

In order to deploy your own version of this website you will need to clone a local copy of the repository. To do this you need to follow the following steps.

- Click on the 'Code' button next to 'Add a file' when you have opened a repository
- To clone your repository by https:// click on the clipboard icon next to the URL.
- Once you have done this, open the terminal of your own repository
  - The current directory will need to be changed to where you want your cloned directory.
- Type 'git clone' into your terminal and then paste in your URL from the earlier steps ```$ git clone https://github.com/Alicepinch/everything-vegan.git```
- Press enter

There are other ways that you can clone a repository and these can be found on the [GitHub docs.](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories)

Once the repository is cloned you will need to ensure that all the packages needed to run this app are installed. To install all packages from requirements.txt file using the following command in terminal.
``` pip3 -r requirements.txt ```

In your local IDE create a file called env.py.
Inside the env.py file create the following environment variables: 

``` 
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", `<your_secret_key>`)
os.environ.setdefault("MONGO_URI", "mongodb+srv://<username>:<password>@<cluster_name>-qtxun.mongodb.net/<database_name>?retryWrites=true&w=majority")
os.environ.setdefault("MONGO_DBNAME", `<your_database_name>`)
```

**As some of this information is sensitive, be sure to create a ".gitignore" file and add "env.py"**

### MongoDB: 


### Heroku deployment:

This repository can now be deployed to Heroku:

To deploy this project to Heroku you will need a Heroku acccount.
Once you have an account please follow the below steps. 

1. In Heroku create a new app and set the region to EU. 

2. In your github project create a requirements.txt file using the terminal command ```pip3 freeze —-local > requirements.txt ``` (This is so Heroku can read all of the web apps that have been used in the project)

4. Create a Procfile by typing ```echo web: python app.py > Procfile``` into the terminal.

5. Add all files to github by typing 'git add .' into the terminal to stage all of your files. Then ```git commit -m "<message here>``` to commit the changes ready to be pushed to GitHub.

6. When all your files are ready to be pushed to github, type ```git push``` in the terminal.

5. Back on your Heroku dashboard for your application, go to 'Deploy'.

6. Within this section, scroll down to 'Deployment method' and select 'Connect to GitHub'

7. In the 'Connect to GitHub' section below - search for the github repository name. When you see the repository name click on the 'Connect' button.

8. Confirm the linking of the heroku app to the correct GitHub repository.

9. In the heroku dashboard for the application, click on "Settings" > "Reveal Config Vars".

10. In the fields fill out the following:

| Key | Value |
 --- | ---
DEBUG | FALSE
IP | 0.0.0.0
MONGO_URI | `mongodb+srv://<username>:<password>@<cluster_name>-qtxun.mongodb.net/<database_name>?retryWrites=true&w=majority`
PORT | 5000
SECRET_KEY | `<your_secret_key>`

## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from 
https://www.pexels.com/

### Acknowledgements

- I received inspiration for this project from X