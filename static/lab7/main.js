function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function(films)  {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');
            let tdTitleRus = document.createElement('td'); 
            let tdTitle = document.createElement('td'); 
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');
        
            tdTitleRus.innerText = films[i].title_ru; 
            tdTitle.innerHTML = films[i].title ? `<i>(${films[i].title})</i>` : '';  // показываем оригинальное название курсивом с скобками
            tdYear.innerText = films[i].year;
        
            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function() {
                editFilm(films[i].id); // передаем правильный ID
            };              
        
            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function(){
                deleteFilm(films[i].id, films[i].title_ru); // передаем правильный ID
            };
        
            tdActions.append(editButton); 
            tdActions.append(delButton);
        
            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);
            tbody.append(tr);
        }
    })
    .catch(function(error) {
        console.error('Error fetching films:', error);
    });
}

function deleteFilm(id, title) {
    if(!confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function (response) {
        if(response.ok) {
            fillFilmList();
        } else {
            console.error('Error deleting film:', response.statusText);
        }
    });
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
    document.getElementById('description-error').innerText = '';
}
  
function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}
  
function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description-error').innerText = '';
    showModal();

}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: parseInt(document.getElementById('year').value, 10),
        description: document.getElementById('description').value
    }

    const url = id === '' ? `/lab7/rest-api/films/` : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(function(rest) {
        if (rest.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return rest.json();
    })
    .then(function(errors) {
        document.getElementById('description-error').innerText = '';
        
        if (errors.title_ru) {
            alert(errors.title_ru);
        }
        if (errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }
        if (errors.year) {
            alert(errors.year);
        }
    });
}


function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
      })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        document.getElementById('description-error').innerText = '';
        showModal();
    });
}
  

  
  