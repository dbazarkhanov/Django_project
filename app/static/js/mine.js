//HTTP Request Configs
const Http = new XMLHttpRequest();
const url='http://127.0.0.1:8000/deleteOffer/';

function deletePoll(id) {
    console.log("clicked")
    Http.open("DELETE", url + id, true);
    Http.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN)
    Http.setRequestHeader("Content-Type", "application/json");

    Http.onload = () => {
      if (Http.readyState == 4 && Http.status == 200) {
          response = JSON.parse(Http.responseText);
          message = response["message"];
          switch(message) {
              case "No id":
                alert("ID not found");
                break;
              case "Poll not found":
                alert("Poll doesn't exist'");
                break;
              case "Success":
                alert("Successfully deleted!");
                window.location.reload();
                break;
          }
      } 
      else {
        console.log(`Error: ${Http.status}`);
        alert(`Oops! A ${Http.status} error has ocurred!`);
      }
    };

    Http.send();
}