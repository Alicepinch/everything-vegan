//Setting global variables
let recipeModal = document.getElementById("delete-recipe-modal");
let accountModal = document.getElementById("delete-account-modal")
let accountBtn = document.getElementsByClassName("account-btn");
let recipeBtn = document.getElementsByClassName("recipe-btn");
let close = document.getElementsByClassName("close");
let cancel = document.getElementsByClassName("cancel")

//Onclick functions to display and hide modal.
$(recipeBtn).click(function(){
    recipeModal.style.display = "block";
})

$(accountBtn).click(function(){
    accountModal.style.display = "block";
})

$(close).click(function(){
    recipeModal.style.display = "none";
    accountModal.style.display = "none";
})

$(cancel).click(function(){
    recipeModal.style.display = "none";
    accountModal.style.display = "none";
})


