

 // Allow form submission
function validateForm() {

    var ageInput = document.getElementById("age");
    var siblingsInput = document.getElementById("siblings");
    var relativesInput = document.getElementById("relatives");

    if (ageInput.value < 0) {
        ageInput.value = 0;
    }

    if (siblingsInput.value < 0) {
        siblingsInput.value = 0;
    }

    if (relativesInput.value < 0) {
        relativesInput.value = 0;
    }

    return true;
}

function updateDeckOptions() {
  var pclassInput = document.getElementById("pclass");
  var deckInput = document.getElementById("deck");
  var selectedClass = parseInt(pclassInput.value);

  // Clear existing options
  deckInput.innerHTML = "";

  // Define deck options based on the selected class
  var deckOptions = [];

  if (selectedClass === 1) {
    deckOptions = ["A", "B", "C", "D", "E"];
  } else if (selectedClass === 2) {
    deckOptions = ["D", "E", "F", "G"];
  } else if (selectedClass === 3) {
    deckOptions = ["D", "E", "F", "G"];
  }

  // Populate the deck options in the select element
  for (var i = 0; i < deckOptions.length; i++) {
    var option = document.createElement("option");
    option.value = deckOptions[i];
    option.text = deckOptions[i];
    deckInput.appendChild(option);
  }
}


function calculatePrice() {
    var pclassInput = document.getElementById("pclass");
    var spouseInput = document.getElementById("spouse");
    var siblingsInput = document.getElementById("siblings");
    var relativesInput = document.getElementById("relatives");
    var priceSpan = document.getElementById("price");

    var ticketPrice = 0;
    var sibPrice = 0;
    var relPrice = 0;
    var classValue = parseInt(pclassInput.value);

    if (classValue === 3) {
        ticketPrice = 7 * 200;
    } else if (classValue === 2) {
        ticketPrice = 13 * 200;
    } else if (classValue === 1) {
        ticketPrice = 35 * 200;
    }

    if (siblingsInput.value !== "" && siblingsInput.value >0) {
        var sibPrice = ticketPrice * siblingsInput.value;

    }

    if (relativesInput.value !== "" && relativesInput.value >0) {
        var relPrice = relativesInput.value * ticketPrice / 2;
    }

    if (spouseInput.value === "1") {
        ticketPrice *= 2;
    }

    ticketPrice += sibPrice + relPrice;

    priceSpan.textContent = "Full price: $" + Math.floor(ticketPrice.toFixed(2));
    }


function deckClassPrice() {
    calculatePrice();
    updateDeckOptions();
    }



updateDeckOptions();

document.querySelector("form").addEventListener("submit", calculatePrice);

document.getElementById("pclass").addEventListener("change", deckClassPrice);
document.getElementById("spouse").addEventListener("change", calculatePrice);
document.getElementById("siblings").addEventListener("change", calculatePrice);
document.getElementById("relatives").addEventListener("change", calculatePrice);
