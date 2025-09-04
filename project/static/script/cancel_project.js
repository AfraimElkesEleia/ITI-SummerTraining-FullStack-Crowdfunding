    const cancelBtn = document.querySelector('.cancel-section .btn-cancel:not([disabled])');
    const modal = document.getElementById('cancelModal');
    const keepBtn = modal.querySelector('.btn-secondary');
    const confirmCancelBtn = modal.querySelector('.btn-cancel');

    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            modal.style.display = 'flex';
        });
    }

    keepBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    confirmCancelBtn.addEventListener('click', () => {
        const projectId = document.getElementById('project-id').value;
        console.log(projectId)
        fetch(`/crowdfunding/api/${projectId}/cancel/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modal.style.display = 'none';
                alert(data.message);
                window.location.href = '/crowdfunding/'
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });
