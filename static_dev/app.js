document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-total-likes], [data-answer-total-likes]').forEach(counter => {
        const value = parseInt(counter.textContent, 10);
        counter.style.color = value >= 0 ? '#198754' : '#dc3545';
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie !== '' && document.cookie !== ' ') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
const likeButtons = document.querySelectorAll('button[data-action-type]');
// console.log(csrftoken) // чисто для дебага, в проде убирать


//likes
for (const item of likeButtons) {
    item.addEventListener('click', (e) => {
        e.preventDefault();

        const answerId = item.dataset.answerId;
        const questionId = item.dataset.questionId;
        const actionType = item.dataset.actionType;

        let url, selector;

        // Определяем тип элемента (вопрос или ответ)
        if (answerId) {
            url = `/answer/${answerId}/like_async`;
            selector = `[data-answer-total-likes="${answerId}"]`;
        } else {
            url = `/${questionId}/like_async`;
            selector = `[data-total-likes="${questionId}"]`;
        }

        const formData = new URLSearchParams();
        formData.append('action', actionType);  // Отправляем тип действия
        // formData.append('csrfmiddlewaretoken', csrftoken);  // Добавьте CSRF в тело

        const request = new Request(
            url,
            {
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                method: 'POST',
                body: formData,
                mode: 'same-origin',
                credentials: 'include',
            }
        );

        fetch(request).then(response => {
            response.json().then((data) => {
                const counter = document.querySelector(selector);
                // console.log('Fetching!')
                if (counter) {
                    counter.textContent = data.total_likes;
                    counter.style.color = data.total_likes >= 0 ? 'green' : 'red';
                    // console.log('Тык!')
                }
                // console.log(counter)
                // counter.textContent = data.total_likes;
            }).catch(error => console.error('Error:', error)
            );
        });
    });
}

//is_correct
document.querySelectorAll('.form-check-input[data-answer-id]').forEach(checkbox => {
    checkbox.addEventListener('change', function(e) {
        const answerId = this.dataset.answerId;
        const isChecked = this.checked;

        const formData = new URLSearchParams();
        formData.append('csrfmiddlewaretoken', csrftoken);

        fetch(`/answer/${answerId}/mark_correct`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                this.checked = !isChecked; // Возвращаем предыдущее состояние
            } else {
                this.checked = data.is_correct;
                this.parentElement.style.color = data.is_correct ? 'green' : 'inherit';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.checked = !isChecked;
        });
    });
});
