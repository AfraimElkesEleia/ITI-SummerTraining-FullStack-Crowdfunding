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
    <form class="reply-form mt-2" data-comment-id="${data.id}" style="display:none;">
        <textarea class="form-control mb-2" placeholder="Write your reply..." required></textarea>
        <button type="submit" class="btn btn-sm btn-success">Submit Reply</button>
    </form>
    <div class="replies mt-2"></div>
`;
            commentsList.prepend(commentCard);
            commentText.value = '';
            initReplyFunctionalityForNewComment(commentCard);
        })
        .catch(err => console.error(err));
});

function initReplyFunctionalityForNewComment(commentElement) {
    const replyBtn = commentElement.querySelector('.reply-btn');
    const replyForm = commentElement.querySelector('.reply-form');
    
    // Reply button functionality
    replyBtn.addEventListener('click', function() {
        const isVisible = replyForm.style.display === 'block';
        replyForm.style.display = isVisible ? 'none' : 'block';
    });
    
    // Reply form submission
    replyForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const text = replyForm.querySelector('textarea').value.trim();
        if (!text) return;
        
        const commentId = replyForm.dataset.commentId;
        fetch(`/crowdfunding/api/${commentId}/add_reply/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'reply_text': text })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const repliesDiv = replyForm.nextElementSibling;
                const replyCard = document.createElement('div');
                replyCard.className = 'card p-2 mb-1 ms-4';
                replyCard.innerHTML = `
                    <strong>${data.user}</strong> 
                    <small class="text-muted ms-2">${data.created_at}</small>
                    <p>${data.text}</p>
                `;
                repliesDiv.appendChild(replyCard);
                replyForm.querySelector('textarea').value = '';
                replyForm.style.display = 'none';
            }
        })
        .catch(err => console.error(err));
    });
}
