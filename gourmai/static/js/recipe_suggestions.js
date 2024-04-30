// Function to apply the 'selected' class to the selected suggestion card
function applySelectedClass() {
    // Retrieve the index of the selected suggestion from local storage
    var selectedSuggestionIndex = localStorage.getItem('selectedSuggestionIndex');
    if (selectedSuggestionIndex !== null) {
        // Retrieve all suggestion cards
        var suggestionCards = document.querySelectorAll('.main-suggestion-card');
        // Remove the 'selected' class from all suggestion cards
        suggestionCards.forEach(function(card) {
            card.classList.remove('selected');
        });
        // Add the 'selected' class to the suggestion card with the stored index
        suggestionCards[selectedSuggestionIndex].classList.add('selected');
    }
    var sideSuggestionContainer = document.getElementById('side-suggestion-form');

    // Scroll to the side suggestion container
    sideSuggestionContainer.scrollIntoView({ behavior: 'smooth' });
}

function submitMain() {
    // Set the value of the 'selectedMain' input field
    var selectedMainSuggestionValue = document.getElementById('selectedMainSuggestion').value;
    var submit = document.getElementById('hiddenSubmitButton')
    
    if (!isPageLoading()) {
        // Page is not loading, so it's safe to submit the form
        // Your form submission code here
        submit.click();
        console.log("Main Submitted");
    } else {
        console.log("Page is still loading. Form submission delayed.");
    }

    submit.removeEventListener('click', onClick);
    console.log("Event fired once, no more click will be handled");
}

// Function to handle selection of a suggestion card
function selectSuggestion(element, suggestion) {
    
    // Remove the 'selected' class from all suggestion cards
    var suggestionCards = document.querySelectorAll('.main-suggestion-card');
    suggestionCards.forEach(function(card) {
        card.classList.remove('selected');
    });

    // Add the 'selected' class to the clicked suggestion card
    element.classList.add('selected');

    // Update the value of the hidden input field with the selected suggestion
    document.getElementById('selectedMainSuggestion').value = suggestion;

    // Store the index of the selected suggestion in local storage
    var selectedSuggestionIndex = Array.from(suggestionCards).indexOf(element);
    localStorage.setItem('selectedSuggestionIndex', selectedSuggestionIndex);

    // Hide the side-suggestion-form
    var sideSuggestionForm = document.getElementById('suggestion-container');
    sideSuggestionForm.style.opacity = '0.0';


    // Preload full-resolution image and submit main suggestion
    preloadFullResImage();
    submitMain();
}

function selectSideSuggestion(element, suggestion) {
    // Remove the 'selected' class from all side suggestion cards
    var sideSuggestionCards = document.querySelectorAll('.side-suggestion-card');
    sideSuggestionCards.forEach(function(card) {
        card.classList.remove('selected');
    });

    // Add the 'selected' class to the clicked side suggestion card
    element.classList.add('selected');

    // Update the value of the hidden input field with the selected suggestion
    document.getElementById('selectedSideSuggestion').value = suggestion;
}


// Function to load the full-resolution image
function loadFullResImage() {
    document.body.style.backgroundImage = "url('static/images/ingredients4.png')"; // Change to full-res image
}

// Function to preload the full-resolution image
function preloadFullResImage() {
    var fullResImage = new Image();
    fullResImage.onload = loadFullResImage; // Load full-res image after it's loaded
    fullResImage.src = "static/images/ingredients4.png"; // Preload the full-res image
}

window.onload = function() {
    applySelectedClass();
}


function resetSelection() {
    // Clear the item stored in local storage
    localStorage.removeItem('selectedSuggestionIndex');

    // Optional: Remove the 'selected' class from all suggestion cards
    var suggestionCards = document.querySelectorAll('.main-suggestion-card');
    suggestionCards.forEach(function(card) {
        card.classList.remove('selected');
    });

    var selectedMainSuggestion = document.getElementById('selectedMainSuggestion');
    if (selectedMainSuggestion) {
        selectedMainSuggestion.value = '';
    }
}


function submitGenerateOnSuggestionForm() {
    
    // Set the hidden div to the main selection value //
    var selectedSuggestionIndex = localStorage.getItem('selectedSuggestionIndex'); // Retrieve from local storage
    document.getElementById('selectedMainSuggestion').value = selectedMainSuggestion;

    // Remove the 'selected' class from all suggestion cards
    var suggestionCards = document.querySelectorAll('.main-suggestion-card');
    suggestionCards.forEach(function(card) {
        card.classList.remove('selected');
        card.onclick = null;
    });
    
    // Hide the side-suggestion-form
    var sideSuggestionForm = document.getElementById('suggestion-container');
    sideSuggestionForm.style.opacity = '0.0';

    document.getElementById('side-suggestion-form').submit();
}





