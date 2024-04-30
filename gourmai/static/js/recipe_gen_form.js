
// Form JS //

var elem = document.getElementById('difficultySlider');
var difficultyValue = document.getElementById('difficultyValue');

var rangeValueDifficulty = function(){
    var newValue = elem.value;
    var target = document.getElementById('difficultyValueInput');

    if (newValue == 0 ) {
        target.innerHTML = "Budget";
    }

    if (newValue == 1 ) {
        target.innerHTML = "Quick & Easy";
    } 

    if (newValue == 2 ) {
        target.innerHTML = "Beginner";
    } 

    if (newValue == 3 ) {
        target.innerHTML = "Intermediate";
    } 

    if (newValue == 4 ) {
        target.innerHTML = "Expert";
    } 

    if (newValue == 5 ) {
        target.innerHTML = "Michelin";
    } 

    // Set the value of the hidden input field to the same as innerHTML
    difficultyValue.value = target.innerHTML;
};

// Attach event listener to the difficulty slider
elem.addEventListener("input", rangeValueDifficulty);



$(document).ready(function() {
    $("#addDietaryRestrictionButton").click(function() {
        var restriction = $("#dietaryRestrictionInput").val().trim(); // Get the user input from the input field and remove leading/trailing whitespace
    
        // Check if the input is empty
        if (restriction === '') {
            // Do nothing if the input is empty
            return;
        }
    
        // Make an AJAX POST request to your Flask route
        $.ajax({
            type: "POST",
            url: "/meal/add-dietary-restriction",
            contentType: "application/x-www-form-urlencoded",
            data: { restriction: restriction }, 
            success: function(response) {
                // Handle success response
                console.log(response);
                // Append the new dietary restriction item to the HTML
                $(".dietary-restrictions-item-box").append('<div class="dietary-restrictions-item">\
                        <div class="dietary-restriction-item">' + restriction + '</div>\
                        <a class="removeDietaryRestrictionButton"><span class="material-symbols-outlined">close</span></a>\
                    </div>');
                // Clear the input field
                $("#dietaryRestrictionInput").val('');
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error(xhr.responseText);
            }
        });
    });
    // Click event for removing dietary restriction (delegated to a parent element)
    $(".dietary-restrictions-item-box").on("click", ".removeDietaryRestrictionButton", function() {
        var item = $(this).siblings(".dietary-restriction-item").text(); // Get the dietary restriction text
        var button = $(this); // Store a reference to the button for later use
        
        // Make an AJAX POST request to remove the dietary restriction
        $.ajax({
            type: "POST",
            url: "/meal/remove-dietary-restriction",
            contentType: "application/x-www-form-urlencoded",
            data: { item: item },
            success: function(response) {
                // Handle success response
                console.log(response);
                // Remove the dietary restriction item from the HTML
                button.closest(".dietary-restrictions-item").remove();
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error(xhr.responseText);
            }
        });
    });
});


function toggleDropdown() {
    event.preventDefault();
    var dropdownContent = document.getElementById("dropdownContent");
    if (dropdownContent.style.display === "block") {
    dropdownContent.style.display = "none";
    } else {
    dropdownContent.style.display = "block";
    }
}

// Close the dropdown when clicking outside
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.style.display === "block") {
        openDropdown.style.display = "none";
        }
    }
    }
}

// Get the checkbox element
var measurementInput = document.getElementById("measurementInput");
// Get the hidden input field
var unitInput = document.getElementById("unitInput");
// Get the units label element
var unitsLabel = document.getElementById("unitsLabel");

// Add an event listener to the checkbox
measurementInput.addEventListener("change", function() {
    // Check if the checkbox is checked
    if (measurementInput.checked) {
        // If checked, set the value of the hidden input field to "imperial"
        unitInput.value = "imperial";
        // Update the units label to "Imperial"
        unitsLabel.textContent = "Imperial";
    } else {
        // If unchecked, set the value of the hidden input field to "metric"
        unitInput.value = "metric";
        // Update the units label to "Metric"
        unitsLabel.textContent = "Metric";
    }

    // AJAX call
    $.ajax({
        type: "POST",
        url: "/meal/update-measurement-units",  // Replace with your Flask route URL
        contentType: "application/x-www-form-urlencoded",
        data: { unit: unitInput.value }, // Pass the unit value as form-encoded data
        success: function(response) {
            // Handle success response
            console.log(response);
        },
        error: function(xhr, status, error) {
            // Handle error response
            console.error(xhr.responseText);
        }
    });
});



// ________________________________ Min max slider ________________________________ //

let minRangeValueGap = 20;
const range = document.getElementById("range_track");
const minval = document.querySelector(".minvalue");
const maxval = document.querySelector(".maxvalue");
const rangeInput = document.querySelectorAll(".min-max-slider");

let minRange, maxRange, minPercentage, maxPercentage;

const minRangeFill = () => {
  range.style.left = (rangeInput[0].value / rangeInput[0].max) * 100 + "%";
};
const maxRangeFill = () => {
  range.style.right =
    180 - (rangeInput[1].value / rangeInput[1].max) * 100 + "%";
};


const setMinValueOutput = () => {
  minRange = parseInt(rangeInput[0].value);
  minval.innerHTML = rangeInput[0].value;
};
const setMaxValueOutput = () => {
  maxRange = parseInt(rangeInput[1].value);
  maxval.innerHTML = rangeInput[1].value;
};

setMinValueOutput();
setMaxValueOutput();
minRangeFill();
maxRangeFill();


rangeInput.forEach((input) => {
  input.addEventListener("input", (e) => {
    setMinValueOutput();
    setMaxValueOutput();

    minRangeFill();
    maxRangeFill();


    if (maxRange - minRange < minRangeValueGap) {
        if (e.target.className === "min") {
            rangeInput[0].value = maxRange - minRangeValueGap;
            setMinValueOutput();
            minRangeFill();

            e.target.style.zIndex = "2";
        } else {
            rangeInput[1].value = minRange + minRangeValueGap;
            e.target.style.zIndex = "2";
            setMaxValueOutput();
            maxRangeFill();

        }

    }
    var hiddenValue = document.getElementById('hiddenTimeInput')
    hiddenValue.value =  rangeInput[0].value + " - " + rangeInput[1].value + " mins";


    console.log(document.getElementById('hiddenTimeInput').value)
  });
});
