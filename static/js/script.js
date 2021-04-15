// Setting global variables
const recipeModal = document.getElementById("delete-recipe-modal");
const accountModal = document.getElementById("delete-account-modal");
const profilePicModal = document.getElementById("update-picture-modal");
const accountBtn = document.getElementsByClassName("account-btn");
const recipeBtn = document.getElementsByClassName("recipe-btn");
const profilePicBtn = document.getElementsByClassName("profile-pic-btn");
const cancel = document.getElementsByClassName("cancel");
const deleteCancel = document.getElementsByClassName("delete-cancel");

// Onclick functions to display and hide modals.
$(recipeBtn).click(function(){
    recipeModal.style.display = "block";
});

$(profilePicBtn).click(function(){
    profilePicModal.style.display = "block";
});

$(accountBtn).click(function(){
    accountModal.style.display = "block";
});

$(cancel).click(function(){
    accountModal.style.display = "none";
    profilePicModal.style.display = "none";
});

$(deleteCancel).click(function(){
    recipeModal.style.display = "none";
});

// Filter drop down menu

$(function (){
    $('#recipes_meal_dropdown').hide();
});

$('#recipeDropDown').click(function () {
    $('#recipes_meal_dropdown').slideToggle();
});

// Blocks confirm form resubmission error

if (window.history.replaceState) {
  window.history.replaceState( null, null, window.location.href );
}

// Hides flash message after a couple of seconds

$(function(){
    setTimeout(function(){
    $('.flash-message').slideUp();
    }, 4000);
  });

// Alerts user their email address has been submitted

$("#subscribe").submit(function(){
  alert("Thank for submitting your email.");
});
