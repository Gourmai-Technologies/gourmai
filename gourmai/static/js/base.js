// Select all elements with the class "accountToolTipTrigger"
const accountToolTipTriggers = document.querySelectorAll(".accountToolTipTrigger");

// Select the tooltip element with the ID "accountToolTip"
const accountToolTip = document.getElementById("accountToolTip");

// Loop through each trigger element and attach the tooltip toggle listener
accountToolTipTriggers.forEach(function(triggerElement) {
    attachTooltipToggleListener(triggerElement, accountToolTip);
});

// Function to toggle tooltip visibility
function toggleTooltip(element) {
    if (element.style.display === "flex") {
        element.style.display = "none";
    } else {
        element.style.display = "flex";
    }
}

// Function to attach tooltip toggle listener
function attachTooltipToggleListener(triggerElement, tooltipElement) {
    triggerElement.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default action if it's a link
        toggleTooltip(tooltipElement);
    });
}
