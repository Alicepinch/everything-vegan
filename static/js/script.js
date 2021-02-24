//Setting global variables
let modal = document.getElementById("delete-modal");
let btn = document.getElementById("modal-btn");
let close = document.getElementsByClassName("close")[0];

//Onclick functions to display and hide modal.
$(btn).click(function(){
    modal.style.display = "block";
})

$(close).click(function(){
    modal.style.display = "none";
})
