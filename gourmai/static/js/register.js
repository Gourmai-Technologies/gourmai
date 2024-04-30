// Function to load the full-resolution image
function loadFullResImage() {
    document.body.style.backgroundImage = "url('../static/images/ingredients6.png')"; // Change to full-res image
}

// Function to preload the full-resolution image
function preloadFullResImage() {
    var fullResImage = new Image();
    fullResImage.onload = loadFullResImage; // Load full-res image after it's loaded
    fullResImage.src = "../static/images/ingredients6.png"; // Preload the full-res image
}

// Call the function to preload the full-resolution image
window.onload = preloadFullResImage;