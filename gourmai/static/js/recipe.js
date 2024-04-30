function updateCounts(data) {
    document.getElementById('upvoteCount').textContent = data.upvotes;
    document.getElementById('downvoteCount').textContent = data.downvotes;
}

function vote(type) {
    fetch('/' + type, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => updateCounts(data))
    .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to all method step elements
    document.querySelectorAll('.method-step').forEach(function(step) {
        step.addEventListener('click', function() {
            // Toggle the "crossed-out" class on the clicked method step
            step.classList.toggle('crossed-out');
        });
    });
});

function autoExpand(textarea) {
    textarea.style.height = 'auto'; // Reset the height to auto
    textarea.style.height = (textarea.scrollHeight) + 'px'; // Set the height to match the content
}

document.querySelectorAll('.minus-button').forEach(function(button) {
    button.addEventListener('click', function() {
        console.log("step clicked!")
        event.preventDefault();
        var index = this.getAttribute('data-index');
        toggleIngredientClass(index);
    });
});

function toggleIngredientClass(index) {
    var ingredientElement = document.getElementById("ingredient-" + index);
    if (ingredientElement) {
        ingredientElement.classList.toggle("crossed-out");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Function to toggle visibility of change input box
    function toggleChangeInputBox(element) {
        // Check if the element is a button within an li or a div
        if (element.classList.contains('change-button')) {
            // For change-button, find the closest li element
            let ingredientItem = element.closest('li.ingredient-item');
            if (ingredientItem) {
                let changeInputBox = ingredientItem.nextElementSibling;
                changeInputBox.classList.toggle('hidden-element');
            } else {
                console.error('Ingredient item not found for change-button', element);
            }
        } else if (element.classList.contains('change-input-box')) {
            // For change-input-box, the ingredient item is the previous sibling
            let ingredientItem = element.previousElementSibling;
            if (ingredientItem && ingredientItem.classList.contains('ingredient-item')) {
                element.classList.toggle('hidden-element');
            } else {
                console.error('Ingredient item not found for change-input-box', element);
            }
        }
    }
    // Attach event listeners to change buttons
    const changeButtons = document.querySelectorAll('.change-button');
    changeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent form submission
            toggleChangeInputBox(this);
        });
    });
    const form = document.querySelector('.ingredientbox');
    form.addEventListener('submit', function(event) {
        let addTextarea = document.querySelector('.add-ingredient-input');
        addTextarea.name = 'additions'; // Set the name attribute directly on the textarea
    });



    let substitutions = [];

    const tickButtons = document.querySelectorAll('.change-input-box button');
    tickButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            let changeInputBox = this.closest('.change-input-box');
            let inputText = changeInputBox.querySelector('.change-input').value.trim();
            let ingredientItem = changeInputBox.previousElementSibling;
            let ingredientName = ingredientItem.dataset.ingredientName;

            if (inputText) {
                // Create a new substitution object and add it to the array
                let substitution = {};
                substitution[ingredientName] = inputText;
                substitutions.push(substitution);

                let substitutionInput = document.querySelector('input[name="substitution"]');
                if (!substitutionInput) {
                    substitutionInput = document.createElement('input');
                    substitutionInput.type = 'hidden';
                    substitutionInput.name = 'substitution';
                    document.querySelector('form').appendChild(substitutionInput); // Append to the form
                }
                substitutionInput.value = JSON.stringify(substitutions);

                toggleChangeInputBox(button);
            } else {
                alert('Please enter a substitute ingredient.');
            }
        });
    });


    let removedIngredients = [];

    const minusButtons = document.querySelectorAll('.minus-button');
    minusButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            let ingredientItem = this.closest('li.ingredient-item');
            let ingredientName = ingredientItem.dataset.ingredientName;

            if (ingredientItem && ingredientName) {
                if (!removedIngredients.includes(ingredientName)) {
                    removedIngredients.push(ingredientName);
                }

                let removalInput = document.querySelector('input[name="removal"]');
                if (!removalInput) {
                    removalInput = document.createElement('input');
                    removalInput.type = 'hidden';
                    removalInput.name = 'removal';
                    document.querySelector('form').appendChild(removalInput); // Append to the form
                }
                removalInput.value = JSON.stringify({ remove: removedIngredients });
            }
        });
    });
});


// Initialize ingredientData with servings
const ingredientData = { servings: 1 };

// Function to parse quantity (numeric, range, or non-numeric)
function parseQuantity(quantityStr) {
    const rangeMatch = quantityStr.match(/^([\d.]+)\s*-\s*([\d.]+)\s*(.*)$/);
    const quantityMatch = quantityStr.match(/^([\d.]+)\s*(.*)$/);

    if (rangeMatch) {
        return {
            lower: parseFloat(rangeMatch[1]),
            upper: parseFloat(rangeMatch[2]),
            unit: rangeMatch[3],
            isRange: true
        };
    } else if (quantityMatch) {
        return {
            value: parseFloat(quantityMatch[1]),
            unit: quantityMatch[2],
            isNumeric: true
        };
    } else {
        return { description: quantityStr, isNumeric: false };
    }
}

// Populate ingredientData object based on the HTML elements
document.querySelectorAll('.dynamic-data').forEach((element) => {
    const ingredient = element.getAttribute('data-ingredient');
    const quantityStr = element.getAttribute('data-quantity');
    const quantity = parseQuantity(quantityStr);

    ingredientData[ingredient] = quantity;
});

// Function to update the displayed ingredients based on servings
function updateIngredients(servings) {
    Object.keys(ingredientData).forEach((ingredient) => {
        if (ingredient !== 'servings') {
            const quantityElement = document.querySelector(`[data-ingredient-name="${ingredient}"] .dbinline`).nextElementSibling;
            if (quantityElement) {
                const ingredientDataItem = ingredientData[ingredient];
                let displayText;

                if (ingredientDataItem.isRange) {
                    const newLower = Math.round(ingredientDataItem.lower * servings);
                    const newUpper = Math.round(ingredientDataItem.upper * servings);
                    displayText = `${newLower} - ${newUpper} ${ingredientDataItem.unit}`;
                } else if (ingredientDataItem.isNumeric) {
                    const newQuantity = Math.round(ingredientDataItem.value * servings);
                    displayText = `${newQuantity} ${ingredientDataItem.unit}`;
                } else {
                    // For non-numeric descriptions, append "per serving"
                    displayText = `${ingredientDataItem.description} per serving`;
                }

                quantityElement.textContent = displayText;
            }
        }
    });

    document.getElementById("servings").textContent = servings;
}


  // Function to update servings based on user input
  function updateServingsFromInput() {
    const servingSizeInput = document.getElementById("serving-size");
    let newServings = parseInt(servingSizeInput.value, 10);

    // Check if newServings is within the allowed range
    if (!isNaN(newServings)) {
        if (newServings > 50) {
            newServings = 50; // Set to maximum if exceeded
        } else if (newServings < 1) {
            newServings = 1; // Set to minimum if below 1
        }
        ingredientData.servings = newServings;
    } else {
        servingSizeInput.value = ingredientData.servings; // Reset to the current servings if input is invalid
    }

    updateIngredients(ingredientData.servings);
}
  
  // Event listeners for servings control buttons
  document.getElementById("decrease-servings").addEventListener("click", () => {
    if (ingredientData.servings > 1) {
      ingredientData.servings--;
      document.getElementById("serving-size").value = ingredientData.servings; // Update the input value
      updateIngredients(ingredientData.servings);
    }
  });
  
  document.getElementById("increase-servings").addEventListener("click", () => {
    if (ingredientData.servings < 50) {
        ingredientData.servings++;
        document.getElementById("serving-size").value = ingredientData.servings; // Update the input value
        updateIngredients(ingredientData.servings);
    }
    });
  
  // Event listener for serving size input changes
  document.getElementById("serving-size").addEventListener("input", updateServingsFromInput);
  
// Set the initial value of the serving size input to the current servings
document.addEventListener("DOMContentLoaded", () => {
    // Function to handle blur event
    function handleInputBlur() {
        let value = parseInt(servingSizeInput.value, 10);
        if (!isNaN(value) && value > 50) {
            servingSizeInput.value = 50;
            ingredientData.servings = 50;
            updateIngredients(ingredientData.servings);
        }
    }

    // Attach blur event listener to the serving size input
    if (servingSizeInput) {
        servingSizeInput.addEventListener('blur', handleInputBlur);
    }

    // Initial update of ingredients based on the default serving size
    updateIngredients(ingredientData.servings);
});

