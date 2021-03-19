//Setting global variables
const recipeModal = document.getElementById("delete-recipe-modal");
const accountModal = document.getElementById("delete-account-modal");
const profilePicModal = document.getElementById("update-picture-modal");
const accountBtn = document.getElementsByClassName("account-btn");
const recipeBtn = document.getElementsByClassName("recipe-btn");
const profilePicBtn = document.getElementsByClassName("profile-pic-btn");
const close = document.getElementsByClassName("close");
const deleteClose = document.getElementsByClassName("delete-close")
const cancel = document.getElementsByClassName("cancel");
const deleteCancel = document.getElementsByClassName("delete-cancel")


//Onclick functions to display and hide modals.
$(recipeBtn).click(function(){
    recipeModal.style.display = "block";
});

$(profilePicBtn).click(function(){
    profilePicModal.style.display = "block";
});

$(accountBtn).click(function(){
    accountModal.style.display = "block";
});

$(close).click(function(){
    accountModal.style.display = "none";
    profilePicModal.style.display = "none";
});

$(cancel).click(function(){
    accountModal.style.display = "none";
    profilePicModal.style.display = "none";
});

$(deleteClose).click(function(){
    recipeModal.style.display = "none";
});

$(deleteCancel).click(function(){
    recipeModal.style.display = "none";
});


// Filter Drop down menu

$(function (){
    $('#recipes_meal_dropdown').hide();
});

$('#recipeDropDown').click(function () {
    $('#recipes_meal_dropdown').slideToggle();
});
