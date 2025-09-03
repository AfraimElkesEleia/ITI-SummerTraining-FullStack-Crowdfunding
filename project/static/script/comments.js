const form = document.getElementById('comment-form');
const commentText = document.getElementById('comment-text');
const commentsList = document.getElementById('comments-list');

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const text = commentText.value.trim();
    if (!text) return;
    const projectId = document.getElementById('project-id').value
    fetch(`/crowdfunding/project_details/${projectId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ comment_text: text })
    })
        .then(response => response.json())
        .then(data => {
            const noComments = document.getElementById('no-comments');
            if (noComments) noComments.remove();

            const commentCard = document.createElement('div');
            commentCard.classList.add('card', 'mb-2', 'p-2');
            commentCard.id = `comment-${data.id}`;
            commentCard.innerHTML = `
               <div class="d-flex align-items-center mb-1">
        <strong>${data.user}</strong>
        <small class="text-muted ms-2">${data.created_at}</small>
        <button class="btn btn-sm btn-outline-primary ms-auto reply-btn" data-comment-id="${data.id}">
            Reply
        </button>
    </div>
    <p>${data.text}</p>
            `;
            commentsList.prepend(commentCard);
            commentText.value = '';
        })
        .catch(err => console.error(err));
});
