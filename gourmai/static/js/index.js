

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

var elem1 = document.getElementById('timeSlider');
var hiddenTimeSliderValue = document.getElementById('hiddenTimeSliderValue');

var rangeValueTime = function(){
    var newValue = elem1.value;
    var target1 = document.getElementById('timeValue');

    if (newValue == 0 ) {
        target1.innerHTML = "Under 15 mins";
    }

    if (newValue == 1 ) {
        target1.innerHTML = "15 - 30 mins";
    } 

    if (newValue == 2 ) {
        target1.innerHTML = "30 - 45 mins";
    } 

    if (newValue == 3 ) {
        target1.innerHTML = "45 - 60 mins";
    } 

    if (newValue == 4 ) {
        target1.innerHTML = "60 - 120 mins";
    } 

    if (newValue == 5 ) {
        target1.innerHTML = "120+ mins";
    } 

    // Set the value of the hidden input field to the same as innerHTML
    hiddenTimeSliderValue.value = target1.innerHTML;
};

// Attach event listener to the time slider
elem1.addEventListener("input", rangeValueTime);





// Other JavaScript code goes here

// Attach event listener to the time slider
elem1.addEventListener("input", rangeValueTime);









// Function to submit the form
function submitRecipeFormFromOutside() {
    submitRecipeForm(); // Call the existing function to submit the form
}

// Optionally, you can also trigger form submission when the user presses Enter key
document.getElementById('recipeInputBox').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        submitRecipeFormFromOutside(); // Call the function to submit the form
    }
});





// Submit Recipe Form // Generate Recipe
function submitRecipeForm() {
    
    var form = document.getElementById('recipeForm');

    // Set recipe input value
    var inputBoxValue = document.getElementById('recipeInputBox').value;
    document.getElementsByName('recipeInput')[0].value = inputBoxValue;

    // Set the difficulty value
    var difficultyValueInput = document.getElementById('difficultyValueInput').innerHTML
    document.getElementById('hiddenDifficultySliderValue').value = difficultyValueInput

    toggleFormVisibility();
    showLoadingBox();
    // Submit the form //
    form.submit();                                                             
}

// Function to hide loading box
function hideLoadingBox() {
    var introBox = document.getElementById('toggleBox');
    var loadingBox = document.getElementById('loadingBox')
    var submitButton = document.querySelector('.submit-icon');
    var settingsButton = document.querySelector('.settings-icon');
    // Change the class of the introBox to inactivebox
    loadingBox.classList.remove('loading-box-active');
    loadingBox.classList.add('loading-box-inactive');

    // Show Intro Box
    introBox.classList.remove('inactive-box');
    introBox.classList.add('active-box');

    // Re-enable the submit and setting buttons
    submitButton.style.pointerEvents = 'auto';
    settingsButton.style.pointerEvents = 'auto';
}

function showLoadingBox() {
    // Init // 
    var form = document.getElementById('recipeForm');
    var introBox = document.getElementById('toggleBox');
    var loadingBox = document.getElementById('loadingBox');
    var submitButton = document.querySelector('.submit-icon');
    var settingsButton = document.querySelector('.settings-icon');

    // Show Loader //
    loadingBox.classList.remove('loading-box-inactive');
    loadingBox.classList.add('loading-box-active');

    // Hide Form // 
    form.classList.remove('active-form');
    form.classList.add('hidden-form');

    // Hide Intro Box // 
    introBox.classList.remove('active-box');
    introBox.classList.add('inactive-box');

    // Disable the submit and setting buttons //
    submitButton.style.pointerEvents = 'none';
    settingsButton.style.pointerEvents = 'none';
}



// Function to toggle the form's visibility
function toggleFormVisibility() {
    var form = document.getElementById('recipeForm')
    var introBox = document.getElementById('toggleBox')

    // Toggle Form Visability // 
    if (form.classList.contains('hidden-form')) {
        form.classList.remove('hidden-form')
        form.classList.add('active-form')
    } else {
        form.classList.remove('active-form')
        form.classList.add('hidden-form')
    }

    // Toggle Intro Box Visablilty //
    if (introBox.classList.contains('active-box')) {
        introBox.classList.remove('active-box')
        introBox.classList.add('inactive-box')
    }
    else {
        introBox.classList.remove('inactive-box')
        introBox.classList.add('active-box')
    }
}

function submitMain() {
    // Set the value of the 'selectedMain' input field
    var selectedMainSuggestionValue = document.getElementById('selectedMainSuggestion').value;
    var submit = document.getElementById('hiddenSubmitButton')
    
    submit.removeEventListener('click', onClick);
    console.log("Event fired once, no more click will be handled");
}


//                              Page Loading                                //
window.onload = function() {
    applySelectedClass();
}

// User Returns to page. 
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        hideLoadingBox();
        
        console.log("User returns using back button...");
    }
});

// User is leaving the page.
window.addEventListener('beforeunload', function() {
    console.log("User leaving the page...");
    showLoadingBox();
});

