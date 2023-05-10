const popup = document.querySelectorAll("td .first");
const modal = document.querySelector(".modal");
const modalContent = document.querySelector(".modal-content")
const close = document.querySelector(".close");

const sellButton = document.querySelector(".sell .first");
const myPrice = document.querySelector(".my-price");
const quantityToSell = document.querySelector(".quantity-to-sell");
const currencyNameInPopUp = document.querySelector(".currencyName");
const currencyPriceInPopUp = document.querySelector(".currencyPrice");
const currencyQuantityInPopUp = document.querySelector(".currencyQuantity");
const totalSum = document.querySelector(".total-sum");

const responseText = document.querySelector(".response")


//HTTP Request Configs
const Http = new XMLHttpRequest();
const url='http://127.0.0.1:8000/sellOffer/';


//walletElement info
var walletElementId = -1;


//Event listeners
for (let i = 0; i < popup.length; i++) {
    popup[i].addEventListener("click", openModal);
}

close.addEventListener("click", closeModal);
sellButton.addEventListener("click", verifyTransaction);
myPrice.addEventListener("change", OnPriceInputChanged);
quantityToSell.addEventListener("change", OnQuantityInputChanged);


//functions
function openModal(e) {
    e.preventDefault();
    modal.style.display = "block";
}

function openPoll(id, name, quantity, price) {
    walletElementId = id;

    currencyNameInPopUp.innerHTML = name;
    currencyPriceInPopUp.innerHTML = "Current market price: $" + price;
    currencyQuantityInPopUp.innerHTML = "You own " + quantity + " " + name;

    var maxPrice = price * 3;
    myPrice.placeholder = "$0.00001 - $" + maxPrice;
    quantityToSell.placeholder = " 0.00001 - " + quantity;

    myPrice.max = maxPrice;
    quantityToSell.max = quantity;
}

function closeModal() {
    modalContent.classList.add("slide-up");
    setTimeout(() => {
        modal.style.display = "none";
        modalContent.classList.remove("slide-up");
    }, 500);
}

function verifyTransaction() {
    var quantity = quantityToSell.value;
    var price = myPrice.value

    if(walletElementId == -1 || quantity == "" || price == "") {
        responseText.innerHTML = "Enter the required fields!";
        return;
    }

    if(Math.round(parseFloat(price * 100000)) < Math.round(parseFloat(0.00001 * 100000))) {
        responseText.innerHTML = "The minimum price is $0.00001";
        return;
    }

    if(Math.round(parseFloat(quantity * 100000)) < Math.round(parseFloat(0.00001 * 100000))) {
        responseText.innerHTML = "The minimum quantity is 0.00001";
        return;
    }

    const body = JSON.stringify({
        'walletElementId': walletElementId,
        'quantity': quantity,
        'price': price
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
              case "Wallet element not found":
                responseText.innerHTML = "The wallet element does not exist!";
                break;
              case "Quantity is less or equal zero":
                responseText.innerHTML = "Quantity should be more than zero!";
                break;
              case "Price is less or equal zero":
                responseText.innerHTML = "Price should be more than zero!";
                break;
              case "The price is too high. The price should not be more than 3 times the market price.":
                responseText.innerHTML = "The price is too high. The price should not be more than 3 times the market price.";
                break;
              case "You are trying to sell more currency than you own":
                responseText.innerHTML = "You are trying to sell more currency than you own!";
                break;
              case "Success":
                alert("Succesful transaction!");
                window.location.reload();
                break;
          }
      } 
      else {
        console.log(`Error: ${Http.status}`);
        alert(`Oops! A ${Http.status} error has ocurred!`);
      }
    };
    Http.send(body);  
}
 
function OnPriceInputChanged() {
    if(quantityToSell.value == ""){
        responseText.innerHTML = "Enter the quantity of currency you would like to offer";
        return;
    }
    if(walletElementId != -1) {
        responseText.innerHTML = "";
        totalSum.value = (quantityToSell.value * myPrice.value).toFixed(3) 
    }
}

function OnQuantityInputChanged() {
    if(myPrice.value == ""){
        responseText.innerHTML = "Enter your price (for 1 currency)";
        return;
    }
    if(walletElementId != -1) {
        responseText.innerHTML = "";
        totalSum.value = (quantityToSell.value * myPrice.value).toFixed(3) 
    } 
}