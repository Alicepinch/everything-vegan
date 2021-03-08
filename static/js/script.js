//Setting global variables
let recipeModal = document.getElementById("delete-recipe-modal");
let accountModal = document.getElementById("delete-account-modal")
let profilePicModal = document.getElementById("update-picture-modal")
let accountBtn = document.getElementsByClassName("account-btn");
let recipeBtn = document.getElementsByClassName("recipe-btn");
let profilePicBtn = document.getElementsByClassName("profile-pic-btn");
let close = document.getElementsByClassName("close");
let cancel = document.getElementsByClassName("cancel")


//Onclick functions to display and hide modals.
$(recipeBtn).click(function(){
    recipeModal.style.display = "block";
})

$(profilePicBtn).click(function(){
    profilePicModal.style.display = "block";
})

$(accountBtn).click(function(){
    accountModal.style.display = "block";
})

$(close).click(function(){
    recipeModal.style.display = "none";
    accountModal.style.display = "none";
    profilePicModal.style.display = "none";
})

$(cancel).click(function(){
    recipeModal.style.display = "none";
    accountModal.style.display = "none";
    profilePicModal.style.display = "none";
})

// Drop down menu

$(function (){
    $('#recipes_meal_dropdown').hide();
})

$('#recipeDropDown').click(function () {
    $('#recipes_meal_dropdown').slideToggle();
});