const donationForm = document.getElementById('donation-form');
const donationSuccess = document.getElementById('donation-success');

donationForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const amountInput = document.getElementById('donation-amount');
    const donateBtn = donationForm.querySelector('button');
    const amount = parseFloat(amountInput.value);
    const projectId = document.getElementById('project-id').value;

    if (!amount || amount <= 0) {
        alert('Enter a valid donation amount.');
        return;
    }
    fetch(`/crowdfunding/api/${projectId}/donate/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: amount })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                donationSuccess.style.display = 'block';
                setTimeout(() => donationSuccess.style.display = 'none', 3000);

                document.querySelector('.donation-stats .stat-item:nth-child(1) .stat-value').textContent = '$' + data.current_total.toFixed(2);
                document.querySelector('.donation-stats .stat-item:nth-child(3) .stat-value').textContent = data.donors_count;

                donationForm.reset();
            } else {
                alert(data.message);
            }
        })
        .catch(err => console.error(err))
        .finally(() => {
            donateBtn.disabled = false;
        });
});

