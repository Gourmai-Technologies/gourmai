const minusButton = document.querySelector('.minusButton');
const plusButton = document.querySelector('.plusButton');
const servingsValue = document.querySelector('.servingsValue');

const minusButton2 = document.querySelector('.minusButton2');
const plusButton2 = document.querySelector('.plusButton2');
const servingsValue2 = document.querySelector('.servingsValue2');

///// Minus Button /////
minusButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent form submission
    let value = parseInt(servingsValue.value);
  
    if (isNaN(value) || value < 1) {
      value = 1;
    } else if (value > 1) {
      value--;
    }
  
    servingsValue.value = value.toString();
    updateQuantities();
});

minusButton2.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent form submission
    let value = parseInt(servingsValue2.value);
  
    if (isNaN(value) || value < 1) {
      value = 1;
    } else if (value > 1) {
      value--;
    }
  
    servingsValue2.value = value.toString();
    updateQuantities2();
});


plusButton.addEventListener('click', function(event) {
    event.preventDefault();
    let value = parseInt(servingsValue.value);
  
    if (isNaN(value) || value < 1) {
        value = 2;
    } else if (value < 50) {
        value++;
    }
  
    servingsValue.value = value.toString();
    updateQuantities();
}); 

plusButton2.addEventListener('click', function(event) {
    event.preventDefault();
    let value = parseInt(servingsValue2.value);
  
    if (isNaN(value) || value < 1) {
        value = 2;
    } else if (value < 50) {
        value++;
    }
  
    servingsValue2.value = value.toString();
    updateQuantities2();
});

///// Input Field /////
servingsValue.addEventListener('input', function(event) {
    this.value = this.value.replace(/[^\d]/g, ''); // Remove non-numeric characters
    updateQuantities();
});

servingsValue.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent form submission when pressing Enter //
    }
});

servingsValue2.addEventListener('input', function(event) {
    this.value = this.value.replace(/[^\d]/g, ''); // Remove non-numeric characters
    updateQuantities2();
});

servingsValue2.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent form submission when pressing Enter //
    }
});

///// Update Ingredient quantities /////
const ingredientQuantities = document.querySelectorAll('.ingredient-quantity');
const ingredientQuantities2 = document.querySelectorAll('.ingredient-quantity2');

function updateQuantities() {
    let multiplier = parseFloat(servingsValue.value);
    if (isNaN(multiplier) || multiplier <= 0) {
        multiplier = 1;
        
    }

    ingredientQuantities.forEach(function(quantity) {
        const originalValue = quantity.getAttribute('data-original-value');
            if (originalValue) {
            const match = originalValue.match(/^(\d+(?:\.\d+)?)\s*(.*)$/);
            if (match) {
                const baseValue = parseFloat(match[1]);
                const unit = match[2];
                const updatedValue = baseValue * multiplier;
                quantity.textContent = updatedValue.toString() + ' ' + unit;
            }
        }
    });
}

function updateQuantities2() {
    let multiplier = parseFloat(servingsValue2.value);
    if (isNaN(multiplier) || multiplier <= 0) {
        multiplier = 1;
        
    }

    ingredientQuantities2.forEach(function(quantity) {
        const originalValue = quantity.getAttribute('data-original-value');
            if (originalValue) {
            const match = originalValue.match(/^(\d+(?:\.\d+)?)\s*(.*)$/);
            if (match) {
                const baseValue = parseFloat(match[1]);
                const unit = match[2];
                const updatedValue = baseValue * multiplier;
                quantity.textContent = updatedValue.toString() + ' ' + unit;
            }
        }
    });
}