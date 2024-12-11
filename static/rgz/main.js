function fillRecipeList() {
    fetch('/rgz/rest-api/recipes/')
    .then(response => response.json())
    .then(recipes => {
        const recipeList = document.getElementById('recipe-list');
        recipeList.innerHTML = ''; // очистить список
        recipes.forEach(recipe => {
            const recipeItem = document.createElement('div');
            recipeItem.className = 'recipe-item';
            recipeItem.id = `recipe-${recipe.id}`; // добавляем уникальный ID
            recipeItem.innerHTML = `
                <h3>${recipe.title}</h3>
                <img src="${recipe.image_url}" alt="${recipe.title}" />
                <p>${recipe.step}</p>
                <p>Ингредиенты: <span id="recipe-${recipe.id}-ingredients"></span></p>
            `;

            const editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function() {
                editRecipe(recipe.id); // передаем правильный ID
            };

            const delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function() {
                deleteRecipe(recipe.id); // передаем правильный ID
            };

            recipeItem.appendChild(editButton);
            recipeItem.appendChild(delButton);
            recipeList.appendChild(recipeItem);

            // Загрузка ингредиентов для конкретного рецепта
            loadRecipeIngredients(recipe.id);
        });
    })
    .catch(error => console.error('Error fetching recipes:', error));
}


function loadIngredients() {
    fetch('/rgz/rest-api/ingredients/')
    .then(response => response.json())
    .then(ingredients => {
        const ingredientSelect = document.getElementById('ingredient-select');
        const editIngredientSelect = document.getElementById('edit-ingredient-select');

        ingredients.forEach(ingredient => {
            const option = document.createElement('option');
            option.value = ingredient.id;
            option.textContent = ingredient.name;
            ingredientSelect.appendChild(option);

            const editOption = option.cloneNode(true);
            editIngredientSelect.appendChild(editOption);
        });
    })
    .catch(error => console.error('Error fetching ingredients:', error));
}

function loadRecipeIngredients(id) {
    fetch(`/rgz/rest-api/recipes/${id}/ingredients`)
    .then(response => response.json())
    .then(ingredients => {
        const ingredientSpan = document.getElementById(`recipe-${id}-ingredients`);
        ingredientSpan.textContent = ingredients.map(i => i.name).join(', ');
    })
    .catch(error => console.error('Error fetching recipe ingredients:', error));
}

function deleteRecipe(id) {
    if (!confirm('Вы уверены, что хотите удалить этот рецепт?')) {
        return;
    }

    fetch(`/rgz/rest-api/recipes/${id}`, { method: 'DELETE' })
    .then(response => {
        if (response.ok) {
            fillRecipeList(); // Обновляем список после удаления
        } else {
            console.error('Error deleting recipe:', response.statusText);
        }
    })
    .catch(error => console.error('Error deleting recipe:', error));
}


let currentRecipeId = null; // Переменная для хранения ID текущего редактируемого рецепта

function showAddRecipeModal() {
    document.getElementById('add-recipe-modal').style.display = 'block';
    clearRecipeForm();
    currentRecipeId = null; // Сбрасываем ID
}

function showEditRecipeModal() {
    document.getElementById('edit-recipe-modal').style.display = 'block';
}

function hideAddRecipeModal() {
    document.getElementById('add-recipe-modal').style.display = 'none';
}

function hideEditRecipeModal() {
    document.getElementById('edit-recipe-modal').style.display = 'none';
}

// Существующая функция addRecipe
function addRecipe() {
    const newRecipe = {
        title: document.getElementById('recipe-title').value,
        step: document.getElementById('recipe-step').value,
        image_url: document.getElementById('recipe-image-url').value,
    };

    fetch('/rgz/rest-api/recipes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newRecipe),
    })
    .then(response => {
        if (response.ok) {
            return response.json().then(data => {
                // Получаем ID нового рецепта
                const recipeId = data.id;
                // Сохраняем ингредиенты
                const selectedIngredients = Array.from(document.getElementById('ingredient-select').selectedOptions).map(option => option.value);
                return saveRecipeIngredients(recipeId, selectedIngredients);
            });
        }
    })
    .then(() => {
        fillRecipeList(); // Обновляем список рецептов
        hideAddRecipeModal(); // Скрываем модальное окно
    });
}

function saveRecipeIngredients(recipeId, ingredients) {
    return fetch(`/rgz/rest-api/recipes/${recipeId}/ingredients`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredients: ingredients }),
    });
}


// Изменяем функцию editRecipe
function editRecipe(id) {
    currentRecipeId = id; // Сохраняем ID рецепта
    fetch(`/rgz/rest-api/recipes/${id}`)
    .then(response => response.json())
    .then(recipe => {
        document.getElementById('edit-recipe-title').value = recipe.title;
        document.getElementById('edit-recipe-step').value = recipe.step;
        document.getElementById('edit-recipe-image-url').value = recipe.image_url;
        
        // Загрузим ингредиенты для редактируемого рецепта
        loadRecipeIngredientsForEdit(id);
        
        showEditRecipeModal(); // показываем модальное окно для редактирования
    });
}

function loadRecipeIngredientsForEdit(id) {
    fetch(`/rgz/rest-api/recipes/${id}/ingredients`)
    .then(response => response.json())
    .then(ingredients => {
        const editIngredientSelect = document.getElementById('edit-ingredient-select');
        Array.from(editIngredientSelect.options).forEach(option => {
            option.selected = ingredients.some(i => i.id == option.value);
        });
    });
}

function updateRecipe() {
    const updatedRecipe = {
        title: document.getElementById('edit-recipe-title').value,
        step: document.getElementById('edit-recipe-step').value,
        image_url: document.getElementById('edit-recipe-image-url').value,
    };

    fetch(`/rgz/rest-api/recipes/${currentRecipeId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedRecipe),
    })
    .then(response => {
        if (response.ok) {
            // Сохраняем ингредиенты после обновления рецепта
            const selectedIngredients = Array.from(document.getElementById('edit-ingredient-select').selectedOptions).map(option => option.value);
            return saveRecipeIngredients(currentRecipeId, selectedIngredients);
        }
    })
    .then(() => {
        // Вместо перезагрузки всего списка обновляем конкретный рецепт в списке
        const recipeItem = document.getElementById(`recipe-${currentRecipeId}`);
        updateRecipeInDOM(recipeItem, updatedRecipe);
        hideEditRecipeModal(); // Скрываем модальное окно
    });
}

// Функция для обновления рецепта в DOM
function updateRecipeInDOM(recipeItem, updatedRecipe) {
    const titleElement = recipeItem.querySelector('h3');
    const imageElement = recipeItem.querySelector('img');
    const stepElement = recipeItem.querySelector('p');

    titleElement.textContent = updatedRecipe.title;
    imageElement.src = updatedRecipe.image_url;
    stepElement.textContent = updatedRecipe.step;

    // Вам также может понадобиться обновить ингредиенты, если они изменились
    loadRecipeIngredients(currentRecipeId);
}

function clearRecipeForm() {
    document.getElementById('recipe-title').value = '';
    document.getElementById('recipe-step').value = '';
    document.getElementById('recipe-image-url').value = '';
}