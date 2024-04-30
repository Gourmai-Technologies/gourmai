const batchSize = 12;

const filterList = document.querySelector('.filter-list');
const searchQueryInput = document.getElementById('search-input');
const searchQuery = document.getElementById('search-query');

const cuisineQueryInput = document.getElementById('cuisine-input');
const cuisineQuery = document.getElementById('cuisine-query');

const ingredientQueryInput = document.getElementById('ingredient-input');
const ingredientQuery = document.getElementById('ingredient-query');

const dietCheckboxes = document.querySelectorAll('.diet-dropdown-content-item input[type="checkbox"]');
const dietFiltersInput = document.getElementById('diet-filters-input');
const dietValues = [];

const allergenCheckboxes = document.querySelectorAll('.allergen-dropdown-content-item input[type="checkbox"]');
const allergenFiltersInput = document.getElementById('allergen-filters-input')
allergenValues = [];

document.querySelector('.apply-filter-button').addEventListener('click', function(event) {
  showLoadingBox();
  event.preventDefault(); // Prevent form submission
  
 
  // Append search query to the filter list
  if (searchQueryInput.value.trim() !== '') {
    const filterText = 'Search: ' + searchQueryInput.value.trim();
    const existingFilterItem = Array.from(filterList.children).find(item => item.textContent.includes('Search:'));

    if (existingFilterItem) {
      // Update the text content of the existing filter item
      existingFilterItem.firstChild.textContent = filterText;
    } else {
      const searchFilterItem = document.createElement('div');
      searchFilterItem.classList.add('filter-item');

      const filterItemText = document.createElement('span');
      filterItemText.textContent = filterText;
      searchFilterItem.appendChild(filterItemText);

      const filterItemRemoveButton = document.createElement('button');
      filterItemRemoveButton.classList.add('filter-item-remove-button');
      filterItemRemoveButton.textContent = 'X';
      filterItemRemoveButton.addEventListener('click', function(event) {
        event.stopPropagation();
        searchFilterItem.remove();
        searchQueryInput.value = '';
        searchQuery.value = '';
        showLoadingBox();
        changeFilters();
      });
      searchFilterItem.appendChild(filterItemRemoveButton);

      filterList.appendChild(searchFilterItem);
    }

    // Update the value of the hidden input
    searchQuery.value = searchQueryInput.value.trim();
  }

  // Append cuisine query to the filter list
  if (cuisineQueryInput.value.trim() !== '') {
    const filterText = 'Cuisine: ' + cuisineQueryInput.value.trim();
    const existingFilterItem = Array.from(filterList.children).find(item => item.textContent.includes(filterText));

    if (!existingFilterItem) {
      const cuisineFilterItem = document.createElement('div');
      cuisineFilterItem.classList.add('filter-item');

      const filterItemText = document.createElement('span');
      filterItemText.textContent = filterText;
      cuisineFilterItem.appendChild(filterItemText);

      const filterItemRemoveButton = document.createElement('button');
      filterItemRemoveButton.classList.add('filter-item-remove-button');
      filterItemRemoveButton.textContent = 'X';
      filterItemRemoveButton.addEventListener('click', function(event) {
        event.stopPropagation();
        cuisineFilterItem.remove();
        const cuisineValue = filterItemText.textContent.replace('Cuisine: ', '');
        const cuisineValues = cuisineQuery.value.split(', ');
        const index = cuisineValues.indexOf(cuisineValue);
        if (index > -1) {
          cuisineValues.splice(index, 1);
          cuisineQuery.value = cuisineValues.join(', ');
        }
        showLoadingBox();
        changeFilters();
      });
      cuisineFilterItem.appendChild(filterItemRemoveButton);

      filterList.appendChild(cuisineFilterItem);

      // Update the value of the hidden input by appending the new cuisine value
      if (cuisineQuery.value.trim() !== '') {
        // Check if the cuisine value already exists in the list
        const cuisineValues = cuisineQuery.value.split(', ');
        if (!cuisineValues.includes(cuisineQueryInput.value.trim())) {
          cuisineQuery.value += ', ' + cuisineQueryInput.value.trim();
        }
      } else {
        cuisineQuery.value = cuisineQueryInput.value.trim();
      }

    }
  }



  // Append ingredient query to the filter list
  if (ingredientQueryInput.value.trim() !== '') {
    const filterText = 'Ingredient: ' + ingredientQueryInput.value.trim();
    const existingFilterItem = Array.from(filterList.children).find(item => item.textContent.includes(filterText));

    if (!existingFilterItem) {
      const ingredientFilterItem = document.createElement('div');
      ingredientFilterItem.classList.add('filter-item');

      const filterItemText = document.createElement('span');
      filterItemText.textContent = filterText;
      ingredientFilterItem.appendChild(filterItemText);

      const filterItemRemoveButton = document.createElement('button');
      filterItemRemoveButton.classList.add('filter-item-remove-button');
      filterItemRemoveButton.textContent = 'X';
      filterItemRemoveButton.addEventListener('click', function(event) {
        event.stopPropagation();
        ingredientFilterItem.remove();
        ingredientQueryInput.value = '';
        ingredientQuery.value = '';
        showLoadingBox();
        changeFilters();
      });
      ingredientFilterItem.appendChild(filterItemRemoveButton);

      filterList.appendChild(ingredientFilterItem);
    }
  }

  // Append selected diet filters to the filter list
  dietCheckboxes.forEach(function(checkbox) {
    if (checkbox.checked) {
      const filterText = 'Diet: ' + checkbox.nextElementSibling.textContent;
      const existingFilterItem = Array.from(filterList.children).find(item => item.textContent.includes(filterText));

      if (!existingFilterItem) {
        const dietFilterItem = document.createElement('div');
        dietFilterItem.classList.add('filter-item');

        const filterItemText = document.createElement('span');
        filterItemText.textContent = filterText;
        dietFilterItem.appendChild(filterItemText);

        const filterItemRemoveButton = document.createElement('button');
        filterItemRemoveButton.classList.add('filter-item-remove-button');
        filterItemRemoveButton.textContent = 'X';
        filterItemRemoveButton.addEventListener('click', function(event) {
          event.stopPropagation();
          dietFilterItem.remove();
          checkbox.checked = false;
          const index = dietValues.indexOf(checkbox.nextElementSibling.textContent);
          if (index > -1) {
            dietValues.splice(index, 1);
            dietFiltersInput.value = dietValues.join(', ');
          }
          showLoadingBox();
          changeFilters();
        });
        dietFilterItem.appendChild(filterItemRemoveButton);

        filterList.appendChild(dietFilterItem);
        dietValues.push(checkbox.nextElementSibling.textContent);
      }
    }
  });

  // Append selected allergen filters to the filter list
  allergenCheckboxes.forEach(function(checkbox) {
    if (checkbox.checked) {
      const filterText = 'Allergen: ' + checkbox.nextElementSibling.textContent;
      const existingFilterItem = Array.from(filterList.children).find(item => item.textContent.includes(filterText));

      if (!existingFilterItem) {
        const allergenFilterItem = document.createElement('div');
        allergenFilterItem.classList.add('filter-item');

        const filterItemText = document.createElement('span');
        filterItemText.textContent = filterText;
        allergenFilterItem.appendChild(filterItemText);

        const filterItemRemoveButton = document.createElement('button');
        filterItemRemoveButton.classList.add('filter-item-remove-button');
        filterItemRemoveButton.textContent = 'X';
        filterItemRemoveButton.addEventListener('click', function(event) {
          event.stopPropagation();
          allergenFilterItem.remove();
          checkbox.checked = false;
          const index = allergenValues.indexOf(checkbox.nextElementSibling.textContent);
          if (index > -1) {
            allergenValues.splice(index, 1);
            allergenFiltersInput.value = allergenValues.join(', ');
          }
          showLoadingBox();
          changeFilters();
        });
        allergenFilterItem.appendChild(filterItemRemoveButton);

        filterList.appendChild(allergenFilterItem);
        allergenValues.push(checkbox.nextElementSibling.textContent);
      }
    }
  });

  // Take the JS values and store them in HTML hidden inputs //
  cuisineQuery.value = cuisineQueryInput.value;
  console.log('Cuisine Query:', cuisineQuery.value);
  
  ingredientQuery.value = ingredientQueryInput.value;
  console.log('Ingredient Query:', ingredientQuery.value);
  
  searchQuery.value = searchQueryInput.value;
  console.log('Search Query:', searchQuery.value);
  
  dietFiltersInput.value = dietValues.join(', ');
  console.log('Diet Filters:', dietFiltersInput.value);
  
  allergenFiltersInput.value = allergenValues.join(', ');
  console.log('Allergen Filters:', allergenFiltersInput.value);


  // Send request for filtered recipe list from Flask //
  $.ajax({
    url: '/discovery/filter',
    method: 'GET',
    data: {
      page: currentPage,
      batch_size: batchSize,
      'diet-filters-input': dietFiltersInput.value,
      'allergen-filters-input': allergenFiltersInput.value,
      'search-query': searchQuery.value,
      'ingredient-query': ingredientQuery.value,
      'cuisine-query': cuisineQuery.value
    },

    success: function(response) {
      
      var contentSection = document.querySelector('.content-section');
      
      // Remove all existing recipe cards
      while (contentSection.firstChild) {
        contentSection.removeChild(contentSection.firstChild);
      }
      
      if (response.recipes.length > 0) {
        var recipes = response.recipes;
        
        // Append the filtered recipe cards
        recipes.forEach(function(recipe) {
          var recipeCard = document.createElement('form');
          recipeCard.id = 'recipe-card';
          recipeCard.className = 'recipe-card';
          recipeCard.action = '/meal/recipe/' + recipe.id;
          recipeCard.method = 'GET';
          recipeCard.onclick = function() {
            this.submit();
          };
          
          var recipeImage = document.createElement('img');
          recipeImage.className = 'recipe-image';
          recipeImage.src = recipe.image;
          recipeImage.alt = 'Image of the recipe';
          recipeCard.appendChild(recipeImage);
          
          var titleButtonBox = document.createElement('div');
          titleButtonBox.className = 'title-button-box';
          
          var recipeTitle = document.createElement('h2');
          recipeTitle.className = 'recipe-title';
          recipeTitle.textContent = recipe.recipe_name;
          titleButtonBox.appendChild(recipeTitle);
          
          recipeCard.appendChild(titleButtonBox);
          
          var recipeIdInput = document.createElement('input');
          recipeIdInput.type = 'hidden';
          recipeIdInput.name = 'recipe_id';
          recipeIdInput.value = recipe.id;
          recipeCard.appendChild(recipeIdInput);
          
          contentSection.appendChild(recipeCard);
        });
        
        currentPage = 2; // Reset the current page to 2 (assuming 1 is the initial page)
      } else {
        // Display a message when no recipes are found
        var noRecipesMessage = document.createElement('h2');
        noRecipesMessage.textContent = 'Sorry, no recipes found. Feel free to generate your own!';
        contentSection.appendChild(noRecipesMessage);
        
        currentPage = 1; // Reset the current page to 1
      }
      hideLoadingBox();
    },
    error: function(xhr, status, error) {
      console.error(error);
      loadingSpinner.style.display = 'none';
      isLoading = false;
      hideLoadingBox();
    }
  });
});

// Request new filtered list //
function changeFilters() {
  showLoadingBox();

  $.ajax({
    url: '/discovery/filter',
    method: 'GET',
    data: {
      page: currentPage,
      batch_size: batchSize,
      'diet-filters-input': dietFiltersInput.value,
      'allergen-filters-input': allergenFiltersInput.value,
      'search-query': searchQuery.value,
      'ingredient-query': ingredientQuery.value,
      'cuisine-query': cuisineQuery.value
    },
    success: function(response) {
      
      var contentSection = document.querySelector('.content-section');
      
      // Remove all existing recipe cards
      while (contentSection.firstChild) {
        contentSection.removeChild(contentSection.firstChild);
      }
      
      if (response.recipes.length > 0) {
        var recipes = response.recipes;
        
        // Append the filtered recipe cards
        recipes.forEach(function(recipe) {
          var recipeCard = document.createElement('form');
          recipeCard.id = 'recipe-card';
          recipeCard.className = 'recipe-card';
          recipeCard.action = '/meal/recipe/' + recipe.id;
          recipeCard.method = 'GET';
          recipeCard.onclick = function() {
            this.submit();
          };
          
          var recipeImage = document.createElement('img');
          recipeImage.className = 'recipe-image';
          recipeImage.src = recipe.image;
          recipeImage.alt = 'Image of the recipe';
          recipeCard.appendChild(recipeImage);
          
          var titleButtonBox = document.createElement('div');
          titleButtonBox.className = 'title-button-box';
          
          var recipeTitle = document.createElement('h2');
          recipeTitle.className = 'recipe-title';
          recipeTitle.textContent = recipe.recipe_name;
          titleButtonBox.appendChild(recipeTitle);
          
          recipeCard.appendChild(titleButtonBox);
          
          var recipeIdInput = document.createElement('input');
          recipeIdInput.type = 'hidden';
          recipeIdInput.name = 'recipe_id';
          recipeIdInput.value = recipe.id;
          recipeCard.appendChild(recipeIdInput);
          
          contentSection.appendChild(recipeCard);
        });
        
        currentPage = 2; // Reset the current page to 2 (assuming 1 is the initial page)
      } else {
        // Display a message when no recipes are found
        var noRecipesMessage = document.createElement('h2');
        noRecipesMessage.textContent = 'Sorry, no recipes found. Feel free to generate your own!';
        contentSection.appendChild(noRecipesMessage);
        
        currentPage = 1; // Reset the current page to 1
      }
      hideLoadingBox();
    },
    error: function(xhr, status, error) {
      console.error(error);
      loadingSpinner.style.display = 'none';
      isLoading = false;
      hideLoadingBox();
    }
  });
}




// _______________________________ Page Loading _______________________________ //

    // Page finishes loading // 
    window.onload = function() {
      applySelectedClass();
  }

  // User Returns to page //
  window.addEventListener('pageshow', function(event) {
      if (event.persisted) {
          console.log("User returns using back button...");

          hideLoadingBox();
      }
  });

  // User is leaving the page.
  window.addEventListener('beforeunload', function() {
      console.log("Page is loading");

      showLoadingBox();
      hideRecipeForm();
  });


  
  function hideLoadingBox() {
      //var introBox = document.getElementById('toggleBox');
      var loadingBox = document.getElementById('loadingBox')
      // var submitButton = document.querySelector('.submit-icon');
      // var settingsButton = document.querySelector('.settings-icon');
      // Change the class of the introBox to inactivebox
      loadingBox.classList.remove('loading-box-active');
      loadingBox.classList.add('loading-box-inactive');

      // Show Intro Box
      // introBox.classList.remove('inactive-box');
      // introBox.classList.add('active-box');

      // Re-enable the submit and setting buttons
      // style.pointerEvents = 'auto';
      // settingsButton.style.pointerEvents = 'auto';
  }

  function showLoadingBox() {
      // Init // 
      // var form = document.getElementById('recipeForm');

      var loadingBox = document.getElementById('loadingBox');
      // var submitButton = document.querySelector('.submit-icon');
      // var settingsButton = document.querySelector('.settings-icon');

      // Show Loader //
      loadingBox.classList.remove('loading-box-inactive');
      loadingBox.classList.add('loading-box-active');

      // Hide Form // 
      // form.classList.remove('active-form');
      // form.classList.add('hidden-form');

      // Disable the submit and setting buttons //
      // submitButton.style.pointerEvents = 'none';
      // settingsButton.style.pointerEvents = 'none';
  }


  // Function to check if the page is loading
  function isPageLoading() {
      return document.readyState === 'loading';
  }