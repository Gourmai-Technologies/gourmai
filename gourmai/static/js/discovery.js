function isBottomOfPage() {
    var scrollPosition = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
    var windowHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight || 0;
    var documentHeight = Math.max(
        document.body.scrollHeight,
        document.body.offsetHeight,
        document.documentElement.clientHeight,
        document.documentElement.scrollHeight,
        document.documentElement.offsetHeight
    );
    var threshold = 100; // Adjust this value as needed
    return (scrollPosition + windowHeight) >= (documentHeight - threshold);
}

var isLoading = false;
var currentPage = 2;
window.addEventListener('scroll', function() {
    if (isBottomOfPage() && !isLoading) {
        
        loadMoreRecipes();
    }
});

var hasMoreRecipes = true;
function loadMoreRecipes() {
    if (!hasMoreRecipes) {
        return;
    }
    var loadingSpinner = document.getElementById('loading-spinner');
    loadingSpinner.style.display = 'flex';
    isLoading = true;
    var batchSize = 12;

    $.ajax({
        url: '/discovery/load-more-recipes',
        method: 'GET',
        data: {
            page: currentPage,
            batch_size: batchSize
        },
        success: function(response) {
            console.log(response);
            if (response.recipes.length > 0) {
                var recipes = response.recipes;
                var contentSection = document.querySelector('.content-section');
                recipes.forEach(function(recipe) {
                    var recipeCard = createRecipeCard(recipe);
                    contentSection.appendChild(recipeCard);
                });
                currentPage++;
            }
            if (!response.has_more) {
                loadingSpinner.style.display = 'none';
                var noMoreRecipesMessage = document.getElementsByClassName('no-more-recipes-message');
                if (noMoreRecipesMessage.length > 0) {
                  noMoreRecipesMessage[0].style.display = 'block';
                }
                hasMoreRecipes = false;
              }
              
            isLoading = false;
        },
        error: function(xhr, status, error) {
            console.error(error);
            loadingSpinner.style.display = 'none';
            isLoading = false;
        }
    });
}

function createRecipeCard(recipe) {
    var recipeCard = document.createElement('form');
    recipeCard.setAttribute('id', 'recipe-card');
    recipeCard.setAttribute('class', 'recipe-card');
    recipeCard.setAttribute('action', `/meal/recipe/${recipe.id}`);
    recipeCard.setAttribute('method', 'GET');
    recipeCard.setAttribute('onclick', 'this.submit()');

    var recipeImage = document.createElement('img');
    recipeImage.setAttribute('class', 'recipe-image');
    recipeImage.setAttribute('src', recipe.image);
    recipeImage.setAttribute('alt', 'Image of the recipe');

    var titleButtonBox = document.createElement('div');
    titleButtonBox.setAttribute('class', 'title-button-box');

    var recipeTitle = document.createElement('h2');
    recipeTitle.setAttribute('class', 'recipe-title');
    recipeTitle.textContent = recipe.recipe_name;

    titleButtonBox.appendChild(recipeTitle);
    recipeCard.appendChild(recipeImage);
    recipeCard.appendChild(titleButtonBox);

    var recipeIdInput = document.createElement('input');
    recipeIdInput.setAttribute('type', 'hidden');
    recipeIdInput.setAttribute('name', 'recipe_id');
    recipeIdInput.setAttribute('value', recipe.id);
    recipeCard.appendChild(recipeIdInput);

    return recipeCard;
}

// Function to submit the form
function submitRecipeFormFromOutside() {
    submitRecipeForm(); // Call the existing function to submit the form
}

// Submit Recipe Form // Generate Recipe
function submitRecipeForm() {
    
    var form = document.getElementById('recipeForm');

    // Set recipe input value
    var inputBoxValue = document.getElementById('recipeInputBox').value;
    document.getElementsByName('recipeInput')[0].value = inputBoxValue;

    // Set the difficulty value
    var difficultyValueInput = document.getElementById('difficultyValueInput').innerHTML
    document.getElementById('hiddenDifficultySliderValue').value = difficultyValueInput

    // Submit the form //
    form.submit();  


    toggleFormVisibility();
    showLoadingBox();                                                           
}
                                                        

// Function to toggle the form's visibility
function toggleFormVisibility() {
    var form = document.getElementById('recipeForm')
    
    // Toggle Form Visability // 
    if (form.classList.contains('hidden-form')) {
        form.classList.remove('hidden-form')
        form.classList.add('active-form')
    } else {
        form.classList.remove('active-form')
        form.classList.add('hidden-form')
    }
}

function showRecipeForm() {
    var form = document.getElementById('recipeForm')

    form.classList.remove('hidden-form')
    form.classList.add('active-form')
}

function hideRecipeForm() {
    var form = document.getElementById('recipeForm')

    form.classList.remove('active-form')
    form.classList.add('hidden-form')
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

document.addEventListener('DOMContentLoaded', function() {
    introJs().setOptions({
        steps: [{
            intro: "Let me show you around!"
        }, 
        {
            element: document.querySelector('.intro-first'),
            intro: "If you know what your after, enter the recipe you want here."
        },
        {
            element: document.querySelector('.intro-second'),
            intro: "Here you can enter ingredients you have on hand and our AI will craft a recipe that includes these."
        },
        {
            element: document.querySelector('.intro-third'),
            intro: "Here you can input what setting your cooking for. It may be a valentine dinner, boxing day lunch, mid day snack or BBQ. Whatever you fancy! Remember you can use natural language and the AI will understand."
        },
        {
            element: document.querySelector('.intro-fourth'),
            intro: "Here specify if your looking for a particular cuisine or style."
        },
        {
            element: document.querySelector('.intro-fith'),
            intro: "Here you can specify any dietary restrictions or allergens you have. You may be vegan or have a nut allergy. Maybe you need heart healthy meals or your bulking for the gym. Fill this out and all your meals going forward will be tailored to this!"
        },
        {
            element: document.querySelector('.intro-sixth'),
            intro: "Here you can specify cooking level. Maybe your learning the ropes and want to start of slow. Or you may be cooking food that could be in the worlds finest restaurants. Choose here."
        },
        {
            element: document.querySelector('.intro-seventh'),
            intro: "Here is your prefered cooking time."
        },
        {
            element: document.querySelector('.intro-eighth'),
            intro: "If you want to be given a selection of options before generating, choose this option. This will allow you to add a side to your recipe too."
        },
        {
            element: document.querySelector('.intro-ninth'),
            intro: "Toggle the measurement units you use here."
        },
        {
            element: document.querySelector('.intro-tenth'),
            intro: "That was lengthy I know, but now you have the power of AI to guide your culinary inspiration. Now generate away, this is free and always will be! Have fun!"
        }
    
    ]
    }).start();
});