function initReplyFunctionality() {
    document.querySelectorAll('.reply-btn').forEach(btn => {
        btn.replaceWith(btn.cloneNode(true));
    });
    
    document.querySelectorAll('.reply-form').forEach(form => {
        form.replaceWith(form.cloneNode(true));
    });

    document.querySelectorAll('.reply-btn').forEach(btn => {
        btn.addEventListener('click', e => {
            const commentId = btn.dataset.commentId;
            const form = document.querySelector(`.reply-form[data-comment-id="${commentId}"]`);
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
        });
    });

    document.querySelectorAll('.reply-form').forEach(form => {
        form.addEventListener('submit', e => {
            e.preventDefault();
            const commentId = form.dataset.commentId;
            const text = form.querySelector('textarea').value.trim();
            if(!text) return;

            fetch(`/crowdfunding/api/${commentId}/add_reply/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'reply_text': text })
            })
            .then(res => res.json())
            .then(data => {
                if(data.success){
                    const repliesDiv = form.nextElementSibling;
                    const replyCard = document.createElement('div');
                    replyCard.className = 'card p-2 mb-1 ms-4';
                    replyCard.innerHTML = `<strong>${data.user}</strong> <small class="text-muted ms-2">${data.created_at}</small><p>${data.text}</p>`;
                    repliesDiv.appendChild(replyCard);
                    form.querySelector('textarea').value = '';
                    form.style.display = 'none';
                }
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    initReplyFunctionality();
});
