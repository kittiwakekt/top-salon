
function clearForm(form){
    const inputs = form.querySelectorAll('input');
    inputs.forEach(element => {
        element.value = '';
    });
    form.querySelectorAll('.error-message').forEach(element => {
        element.textContent = '';
    });
}
// Функция для открытия модального окна
function openMasterModal() {
    const modal = document.getElementById('masterModal');
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    
    // Показываем модальное окно
    modal.style.display = 'block';
    
    // Добавляем затемняющий фон
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden'; // Блокируем прокрутку
    
    // Добавляем класс для анимации
    setTimeout(() => {
        modal.classList.add('modal-visible');
        overlay.classList.add('overlay-visible');
    }, 10);
}

// Функция для закрытия модального окна
function closeMasterModal() {
    const modal = document.getElementById('masterModal');
    const overlay = document.querySelector('.modal-overlay');

    clearForm(modal);

    // Скрываем с анимацией
    modal.classList.remove('modal-visible');
    if (overlay) overlay.classList.remove('overlay-visible');
    
    // После анимации полностью скрываем
    setTimeout(() => {
        modal.style.display = 'none';
        if (overlay) document.body.removeChild(overlay);
        document.body.style.overflow = ''; // Восстанавливаем прокрутку
    }, 300);
}

const btnClose = document.querySelector('#btn-close')
const spanClose = document.querySelector('.close')

if(btnClose) {
    btnClose.addEventListener('click', closeMasterModal)
}

if(spanClose) {
    spanClose.addEventListener('click', closeMasterModal)
}

document.addEventListener('keydown', function(event){
    if(event.key === 'Escape'){
        closeMasterModal();
    }
})

document.addEventListener('click', function(event){
        if(event.target === document.querySelector('#masterModal')){
            closeMasterModal();
        }
})

const modalForm = document.getElementById('masterForm');
modalForm.addEventListener('submit', function(event){
    event.preventDefault();
    this.querySelectorAll('.error-message').forEach(element => {
        element.textContent = '';
    });

    let isValid = true;

    const firstName = document.getElementById('id_first_name').value;
    if(firstName.length<2){
        isValid = false;
        document.getElementById('firstNameError').textContent = 'Error';
    }

    const exp = document.getElementById('id_experience').value;
    if(exp > 50 || exp < 0){
        isValid = false;
        document.getElementById('experienceError').textContent = 'Error';
    }

    if(isValid){
        const formData = new FormData();
        formData.append('first_name', document.getElementById('id_first_name').value.trim());
        formData.append('last_name', document.getElementById('id_last_name').value.trim());
        formData.append('specialization', document.getElementById('id_specialization').value.trim());
        formData.append('salon', parseInt(document.getElementById('id_salon').value.trim()));
        formData.append('experience', parseInt(document.getElementById('id_experience').value.trim()));
        sendData(formData);
        clearForm(this);

    }

})

function getCSRFToken(){
    return(document.querySelector('[name=csrfmiddlewaretoken]').value);
}

function sendData(formData){

    fetch('/api/master/add', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(),
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('HTTP error'); // ✅ Попадёт в catch
        }
        return(response.json());
    })
    .then(data => {
        closeMasterModal();
        // window.location.reload();  
        
        addCard(data.master);


    })
    .catch(error => {
        console.error('Поймано в catch:', error);
    })
}

function addCard(master){
    const list = document.querySelector('#master-list');
    const divCol = document.createElement('div');
    divCol.classList.add('col-md-4', 'mb-4');
    list.appendChild(divCol);

    const divCard = document.createElement('div');
    divCard.classList.add('card', 'h-100');
    divCol.appendChild(divCard);

    const divBody = document.createElement('div');
    divBody.classList.add('card-body', 'text-center');
    divCard.appendChild(divBody);

    const divIcon = document.createElement('div');
    divIcon.classList.add('mb-3');
    divBody.appendChild(divIcon);

        const iIcon = document.createElement('div');
        iIcon.classList.add('bi', 'bi-person-circle', 'icon-large');
        divIcon.appendChild(iIcon);

    const title = document.createElement('h5');
    title.classList.add('card-title');
    divBody.appendChild(title);

        const textName = document.createTextNode(master.name);
        title.appendChild(textName);

    const p = document.createElement('p');
    p.classList.add('text-muted');
    divBody.appendChild(p);

        const textCpec = document.createTextNode(master.specialization);
        p.appendChild(textCpec);

    const divRating = document.createElement('div');
    divRating.classList.add('rating', 'mb-2');
    divBody.appendChild(divRating);

    
    for(i=0; i<5; i++){
        const biStar = document.createElement('i');
        biStar.classList.add('bi', 'bi-star');
        divRating.appendChild(biStar);
    }

    const span = document.createElement('span');
    span.classList.add('ms-1');
    divRating.appendChild(span);

        const textSpan = document.createTextNode('(0.0)');
        span.appendChild(textSpan);


    const pCard = document.createElement('p');
    pCard.classList.add('card-text');
    divBody.appendChild(pCard);
    
    const divBtn = document.createElement('div');
    divBtn.classList.add('btn-group');
    divBody.appendChild(divBtn);

    const btnDetail = document.createElement('a');
    btnDetail.classList.add('btn', 'btn-outline-primary', 'btn-sm');
    btnDetail.href = '/masters/' + master.id + '/';
    divBtn.appendChild(btnDetail);
    btnDetail.appendChild(document.createTextNode('Подробнее'))
}
