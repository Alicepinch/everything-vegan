//Setting global variables
let recipeModal = document.getElementById("delete-recipe-modal");
let accountModal = document.getElementById("delete-account-modal");
let profilePicModal = document.getElementById("update-picture-modal");
let accountBtn = document.getElementsByClassName("account-btn");
let recipeBtn = document.getElementsByClassName("recipe-btn");
let profilePicBtn = document.getElementsByClassName("profile-pic-btn");
let close = document.getElementsByClassName("close");
let deleteClose = document.getElementsByClassName("delete-close")
let cancel = document.getElementsByClassName("cancel");
let deleteCancel = document.getElementsByClassName("delete-cancel")


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

// Profile page tabs to display different things

$( document ).ready(function() {
    $('.saved-recipe-card').hide();
});

$('.saved-recipes').click(function () {
    $('.profile-recipe-card').hide();
    $('#no-recipes').hide();
    $('.saved-recipe-card').show();
});

$('.all-recipes').click(function () {
    $('#no-recipes').show();
    $('.profile-recipe-card').show();
    $('.saved-recipe-card').hide();
})

