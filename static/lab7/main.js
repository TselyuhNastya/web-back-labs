function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            for(let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                
                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');
                
                tdTitleRus.innerText = films[i].title_ru;
                tdYear.innerText = films[i].year;

                //отображение оригинального названия
                if (films[i].title !== films[i].title_ru) {
                    tdTitle.innerHTML = `<span class="original-title">${films[i].title}</span>`;
                } else {
                    tdTitle.innerHTML = `<span class="original-title">${films[i].title_ru}</span>`;
                }

                //кнопки
                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                editButton.onclick = function() {
                    editFilm(films[i].id); 
                };
                
                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = function() {
                    deleteFilm(films[i].id, films[i].title_ru); 
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
            console.error('Ошибка при загрузке фильмов:', error);
        });
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function () {
        fillFilmList();
    })
    .catch(function(error) {
        console.error('Ошибка при удалении фильма:', error);
    });
}

function clearAllErrors() {
    document.getElementById('title_ru_error').innerText = '';
    document.getElementById('title_error').innerText = '';
    document.getElementById('year_error').innerText = '';
    document.getElementById('description_error').innerText = '';
    
    document.getElementById('title_ru').classList.remove('error-border');
    document.getElementById('title').classList.remove('error-border');
    document.getElementById('year').classList.remove('error-border');
    document.getElementById('description').classList.remove('error-border');
}

function showModal() {
    document.getElementById('film-modal').style.display = 'block';
    clearAllErrors();
}

function hideModal() {
    document.getElementById('film-modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

//готовим форму для добавления нового фильма 
function addFilm() {
    document.getElementById('film-id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

//функция отправки данных фильма на сервер (добавление или обновление)
function sendFilm() {
    const id = document.getElementById('film-id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title_ru').value.trim(),
        year: document.getElementById('year').value,
        description: document.getElementById('description').value.trim()
    };

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    clearAllErrors();

    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if (errors && Object.keys(errors).length > 0) {
            for (const [field, message] of Object.entries(errors)) {
                const errorElement = document.getElementById(`${field}_error`); //элемент ошибки
                const inputElement = document.getElementById(field); //поле ввода
                
                if (errorElement && inputElement) {
                    errorElement.innerText = message;
                    inputElement.classList.add('error-border');
                }
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка при отправке данных:', error);
    });
}

//функция загружает данные существующего фильма для редактирования
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function (data) {
            return data.json();
        })
        .then(function (film) {
            document.getElementById('film-id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title_ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильма:', error);
        });
}