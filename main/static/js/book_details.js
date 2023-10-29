const likeForm = document.querySelector('#likeform');
const commentForm = document.querySelector('#commentform');
const bookId = document.querySelector('.book-details').dataset.id;
const username = document.querySelector('.book-details').dataset.username;
const likeButton = likeForm.querySelector('input[type="submit"]');

likeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const response = await fetch(`/like/${bookId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    });
    const data = await response.json();
    if (data.liked) {
        likeButton.value = `Unlike  ${data.likes_count}`;
        likeButton.className = 'btn btn-danger';
    } else {
        likeButton.value = `Like ${data.likes_count}`;
        likeButton.className = 'btn btn-outline-danger';
    }
});

commentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const comment = commentForm.querySelector('textarea').value;
    const response = await fetch(`/create-comment-ajax/${bookId}/`, {
        method: 'POST',
        body: new FormData(commentForm),
    });
    const data = await response.json();
    if (data.success) {
        const commentList = document.querySelector('.comment-list');
        const commentItem = document.createElement('li');
        commentItem.className = 'card mb-2';
        commentItem.style.width = '250px';
        commentItem.innerHTML = `
            <div class="card-body">
                <p class="card-title">
                    ${username}
                </p>
                <p class="card-text">${comment}</p>
            </div>
        `;
        commentList.appendChild(commentItem);
        commentForm.querySelector('textarea').value = '';
    } else {
        alert("Unable to add comment!");
    }
}
);