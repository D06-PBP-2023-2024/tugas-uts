const likeForm = document.querySelector('#likeform');
const bookId = document.querySelector('.book-details').dataset.id;
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