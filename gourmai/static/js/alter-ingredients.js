document.addEventListener('DOMContentLoaded', function() {
    const recipeName = document.getElementById('recipeName');
    const buttons = document.querySelectorAll('#changeIngredientButton');
    const regenRecipeButton = document.getElementById('regenRecipeButton');

    regenRecipeButton.addEventListener('click', function() {
        const originalRecipeID = document.getElementById('recipeID')
        const ingredients = getIngredients();
        console.log(ingredients)

        alterRecipeData = {
            recipeID :  originalRecipeID.value,
            ingredients: ingredients
        }

        $.ajax({
            url: '/meal/generate-altered-recipe',
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(alterRecipeData),

            success: function(response) {
                window.location.href = '/meal/recipe/' + response.recipe_id;
            },
            error:  function(xhr, status, error) {
                console.log('get_altered_recipe() failed');
                console.log(error);
            }

        })
    });


    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            const ingredientItem = button.closest('.ingredient-item-box');
            const ingredientNameElement = ingredientItem.querySelector('.ingredient-name strong');
            const originalItemName = ingredientItem.querySelector('.ingredient-name').getAttribute('original-item');
            const ingredientName = ingredientNameElement.textContent;
            


            const data = {
                ingredientName: ingredientName,
                recipeName: recipeName.textContent
            };

            $.ajax({
                url: '/meal/generate-ingredient-alternatives',
                method: 'POST',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(data),
                success: function(response) {
                    regenRecipeButton.style.display = 'block'
    
                    button.style.display = 'none';

                    // Find the substitutions list relative to the clicked button
                    const substitutionsList = ingredientItem.querySelector('.substitutions-list');
                    

                    // Clear any existing substitutions
                    substitutionsList.innerHTML = '';

                    // Check if the original item is in the substitutions list
                    const isOriginalItemInList = response.substitutions.includes(originalItemName);

                    // Append the original item to the substitutions list if it's not already present
                    if (!isOriginalItemInList) {
                        const originalItem = document.createElement('div');
                        originalItem.classList.add('substitution-item');
                        originalItem.addEventListener('click', function() {
                            ingredientNameElement.textContent = originalItemName;
                            
                        });
                        originalItem.textContent = originalItemName;
                        substitutionsList.appendChild(originalItem);
                    }

                    // Append the new substitutions to the list
                    response.substitutions.forEach(function(substitution) {
                        const substitutionItem = document.createElement('div');
                        substitutionItem.classList.add('substitution-item');

                        substitutionItem.addEventListener('click', function() {
                            const ingredientItemBox = substitutionItem.closest('.ingredient-item-box');
                            const ingredientNameElement = ingredientItemBox.querySelector('.ingredient-name strong');
                            ingredientNameElement.textContent = substitution;
                            ingredientNameElement.setAttribute('new-item', substitution);
                            //console.log(ingredientNameElement.getAttribute('new-item'));


                            //const ingredients = getIngredients();
                            const hiddenInput = ingredientItemBox.querySelector('.changed-value');
                            hiddenInput.value = substitution;
                        });
                        substitutionItem.textContent = substitution;
                        substitutionsList.appendChild(substitutionItem);
                    });
                },
                error: function(xhr, status, error) {
                    console.log('Request failed');
                    console.log(error);
                    // Handle the error
                }
            });
        });
    });


    function getIngredients() {
        const ingredients = [];
        const ingredientItems = document.querySelectorAll('.ingredient-item-box');
        
        ingredientItems.forEach(function(item) {
          const ingredientNameElement = item.querySelector('.ingredient-name strong');
          const ingredientName = ingredientNameElement.textContent;
          console.log('adding ' + ingredientName);
          ingredients.push(ingredientName);
        });
        
        const halfLength = Math.ceil(ingredients.length / 2);
        const secondHalfIngredients = ingredients.slice(halfLength);
        
        console.log(secondHalfIngredients);
        return secondHalfIngredients;
      }
});