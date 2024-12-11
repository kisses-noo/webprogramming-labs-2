function fillRecipeList() {
    fetch('/rgz/rest-api/recipes/')
    .then(function (response) {
        return response.json();
    })
    .then(function(recipes)  {
        const recipeList = document.getElementById('recipe-list');
        recipeList.innerHTML = ''; // очистить список
        for (let i = 0; i < recipes.length; i++) {
            const recipeItem = document.createElement('div');
            recipeItem.className = 'recipe-item';
            recipeItem.innerHTML = `
                <h3>${recipes[i].title}</h3>
                <img src="${recipes[i].image_url}" alt="${recipes[i].title}" />
                <p>${recipes[i].step}</p>
            `;
            
            const editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function() {
                editRecipe(recipes[i].id); // передаем правильный ID
            };

            const delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function() {
                deleteRecipe(recipes[i].id); // передаем правильный ID
            };

            recipeItem.appendChild(editButton);
            recipeItem.appendChild(delButton);
            recipeList.appendChild(recipeItem);
        }
    })
    .catch(function(error) {
        console.error('Error fetching recipes:', error);
    });
}

function deleteRecipe(id) {
    if (!confirm('Вы уверены, что хотите удалить этот рецепт?')) {
        return;
    }

    fetch(`/rgz/rest-api/recipes/${id}`, { method: 'DELETE' })
    .then(function (response) {
        if (response.ok) {
            fillRecipeList(); // Обновляем список после удаления
        } else {
            console.error('Error deleting recipe:', response.statusText);
        }
    });
}

function showAddRecipeModal() {
    document.getElementById('add-recipe-modal').style.display = 'block';
    clearRecipeForm();
}

function hideAddRecipeModal() {
    document.getElementById('add-recipe-modal').style.display = 'none';
}

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
    .then(function (response) {
        if (response.ok) {
            fillRecipeList(); // Обновляем список рецептов
            hideAddRecipeModal(); // Скрываем модальное окно
        }
    });
}

function editRecipe(id) {
    fetch(`/rgz/rest-api/recipes/${id}`)
    .then(function (response) {
        if (response.ok) {
            response.json().then(function(recipe) {
                document.getElementById('recipe-title').value = recipe.title;
                document.getElementById('recipe-step').value = recipe.step;
                document.getElementById('recipe-image-url').value = recipe.image_url;
                showAddRecipeModal(); // показать модальное окно
            });
        }
    });
}

function clearRecipeForm() {
    document.getElementById('recipe-title').value = '';
    document.getElementById('recipe-step').value = '';
    document.getElementById('recipe-image-url').value = '';
}
