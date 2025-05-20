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
const likeButtons = document.querySelectorAll('button[data-question-id]');
console.log(likeButtons)

for (const item of likeButtons) {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const request = new Request(
            `/${item.dataset.questionId}/like_async`,
            {
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                method: 'POST',
                body: new URLSearchParams(),
                mode: 'same-origin',
                credentials: 'include',
            }
        );

        fetch(request).then(response => {
            response.json().then((data) => {
                const counter = document.querySelector(`p[data-like-count="${item.dataset.questionId}"]`);
                console.log(counter)
                counter.innerHTML = data.likes_count;
            }).catch(error => console.error('Error:', error)
            );
        });
    });
}