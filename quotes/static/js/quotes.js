console.log('quotes.js loaded');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
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

function updateVoteUI(id, status, likes, dislikes) {
    const likeButtons = document.querySelectorAll(`.like-btn[data-id="${id}"]`);
    const dislikeButtons = document.querySelectorAll(`.dislike-btn[data-id="${id}"]`);

    likeButtons.forEach(likeBtn => {
        const likeCount = likeBtn.querySelector('.like-count');
        if (likeCount) likeCount.textContent = likes;
        likeBtn.classList.remove('liked');
    });

    dislikeButtons.forEach(dislikeBtn => {
        const dislikeCount = dislikeBtn.querySelector('.dislike-count');
        if (dislikeCount) dislikeCount.textContent = dislikes;
        dislikeBtn.classList.remove('disliked');
    });

    if (status === "liked") {
        likeButtons.forEach(btn => btn.classList.add('liked'));
    } else if (status === "disliked") {
        dislikeButtons.forEach(btn => btn.classList.add('disliked'));
    }
}

function handleVote(btn) {
    console.log('Vote button clicked', btn.dataset);

    const id = btn.dataset.id;
    const action = btn.dataset.action;
    const url = `/quote/${id}/${action}/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(res => res.json())
    .then(data => {
        console.log('Response data:', data);

        if (data.status) {
            updateVoteUI(id, data.status, data.likes, data.dislikes);
        }
    })
    .catch(error => console.error('Fetch error:', error));
}

function loadRandomQuote() {
    console.log('Loading random quote');

    const url = document.getElementById('random-quote-btn').dataset.url;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            console.log('Random quote data:', data);

            if (data.error) {
                alert(data.error);
                return;
            }

            const quoteElement = document.querySelector('.quote');
            if (quoteElement) {
                quoteElement.innerHTML = `
                    <blockquote>
                        <p class="quote-text">${data.text}</p>
                        <div class="quote-views">👁️ ${data.views}</div>
                        <em class="quote-source">${data.source}</em>
                    </blockquote>
                    <div class="quote-container">
                        <div class="vote-buttons">
                            <button class="vote-btn like-btn ${data.voted === 1 ? 'liked' : ''}" 
                                    data-id="${data.id}" data-action="like">
                                👍 <span class="like-count">${data.likes}</span>
                            </button>
                            <button id="random-quote-btn" data-url="${url}">
                                Хочу цитату
                            </button>
                            <button class="vote-btn dislike-btn ${data.voted === -1 ? 'disliked' : ''}" 
                                    data-id="${data.id}" data-action="dislike">
                                👎 <span class="dislike-count">${data.dislikes}</span>
                            </button>
                        </div>
                    </div>
                `;

                attachEventListeners();
            }
        })
        .catch(error => console.error('Random quote error:', error));
}

function attachEventListeners() {
    console.log('Attaching event listeners');

    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            handleVote(btn);
        });
    });

    const randomBtn = document.getElementById('random-quote-btn');
    if (randomBtn) {
        randomBtn.addEventListener('click', (e) => {
            e.preventDefault();
            loadRandomQuote();
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');
    attachEventListeners();
});
