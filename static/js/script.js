//Setting global variables
let modal = document.getElementById("delete-modal");
let btn = document.getElementsByClassName("modal-btn");
let close = document.getElementsByClassName("close");
let cancel = document.getElementById("cancel")

//Onclick functions to display and hide modal.
$(btn).click(function(){
    modal.style.display = "block";
})

$(close).click(function(){
    modal.style.display = "none";
})

$(cancel).click(function(){
    modal.style.display = "none";
})


