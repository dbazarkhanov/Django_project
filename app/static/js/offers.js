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
const responseText = document.querySelector(".response")


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
iWantToPayInput.addEventListener("change", OnPayInputChanged);
iWantToGetInput.addEventListener("change", OnGetInputChanged);


//functions
function openModal(e) {
    e.preventDefault();
    modal.style.display = "block";
}

function openPoll(id, name, quantity, price) {
    pollId = id;
    pollPrice = price;
    currencyNameInPopUp.innerHTML = name;
    currencyPriceInPopUp.innerHTML = "Price: $" + price;
    currencyQuantityInPopUp.innerHTML = "Available: " + quantity;

    var maxValue = quantity * price;
    iWantToPayInput.placeholder = "$0.5 - $" + maxValue.toFixed(5);
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
    var payment = iWantToPayInput.value;

    if(pollId == -1 || quantity == "") {
        alert("Enter the required fields!");
        return;
    }

    if(payment < 0.5) {
        responseText.innerHTML = "The minimum payment is $0.5";
        return;
    }

    const body = JSON.stringify({
        'pollId': pollId,
        'quantity': quantity
    });

    //console.log(body);

    Http.open("POST", url, true);
    Http.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN)
    Http.setRequestHeader("Content-Type", "application/json");

    Http.onload = () => {
      if (Http.readyState == 4 && Http.status == 200) {
          response = JSON.parse(Http.responseText);
          message = response["message"];
          switch(message) {
              case "Poll not found":
                responseText.innerHTML = "The poll does not exist!";
                break;
              case "Quantity is less or equal zero":
                responseText.innerHTML = "Quantity should be more than zero!";
                break;
              case "Not enough balance":
                balance = response["balance"];
                responseText.innerHTML = "Not enough balance! Current balance is $" + balance.toFixed(3);
                break;
              case "You are trying to buy more currency than available":
                responseText.innerHTML = "You are trying to buy more currency than available!";
                break;
              case "Success":
                alert("Succesful transaction!");
                window.location.reload();
                break;
          }

      } else {
        console.log(`Error: ${Http.status}`);
        alert(`Oops! A ${Http.status} error has ocurred!`);
      }
    };

    Http.send(body);
    }

   function OnPayInputChanged() {
        if(pollId != -1 && pollPrice != -1) {
            responseText.innerHTML = "";
            iWantToGetInput.value = (iWantToPayInput.value / pollPrice).toFixed(5);
        }
}