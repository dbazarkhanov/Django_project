const popup = document.querySelectorAll("td .first");
const modal = document.querySelector(".modal");
const modalContent = document.querySelector(".modal-content")
const close = document.querySelector(".close");
const buyButton = document.querySelector(".buy .first");
const iWantToPayInput = document.querySelector(".toPayPrice");
const iWantToGetInput = document.querySelector(".toGetQuantity");
const currencyNameInPopUp = document.querySelector(".currencyName");
const currencyPriceInPopUp = document.querySelector(".currencyPrice");
const currencyQuantityInPopUp = document.querySelector(".currencyQuantity");

//HTTP Request Configs
const Http = new XMLHttpRequest();
const url='http://127.0.0.1:8000/buyOffer/';


//poll info
var pollId = -1;
var pollPrice = -1;


//Event listeners
for (let i = 0; i < popup.length; i++) {
    popup[i].addEventListener("click", openModal);
}

close.addEventListener("click", closeModal);
buyButton.addEventListener("click", verifyTransaction);
iWantToPayInput.addEventListener("change", OnPayInputChanged)


//functions
function openModal(e) {
    e.preventDefault();
    modal.style.display = "block";
}

function openPoll(id, name, quantity, price) {
    pollId = id;
    pollPrice = price;
    currencyNameInPopUp.innerHTML = name;
    currencyPriceInPopUp.innerHTML = "Price: $ " + price;
    currencyQuantityInPopUp.innerHTML = "Available: " + quantity;

    var maxValue = quantity * price;
    iWantToPayInput.placeholder = "$0.5 - $" + maxValue;
    iWantToPayInput.max = maxValue;
    iWantToGetInput.max = quantity;
}

function closeModal() {
    modalContent.classList.add("slide-up");
    setTimeout(() => {
        modal.style.display = "none";
        modalContent.classList.remove("slide-up");
    }, 500);
}

function verifyTransaction() {
    var quantity = iWantToGetInput.value;

    const body = JSON.stringify({
        pollId: pollId,
        quantity: quantity,
    });

    Http.open("POST", url);
    Http.setRequestHeader("Content-Type", "application/json");

    Http.onload = () => {
      if (Http.readyState == 4 && Http.status == 201) {
        console.log(JSON.parse(Http.responseText));
      } else {
        console.log(`Error: ${Http.status}`);
      }
    };

    Http.send(body);
}

function OnPayInputChanged() {
    if(pollId != -1 && pollPrice != -1) {
        iWantToGetInput.value = (iWantToPayInput.value / pollPrice).toFixed(5);
    }
    
}