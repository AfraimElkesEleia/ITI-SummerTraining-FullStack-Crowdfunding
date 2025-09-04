    const starsContainer = document.getElementById('rating-stars');
    if (starsContainer) {
        const stars = document.querySelectorAll('.star');
        const selectedRating = document.getElementById('selected-rating');
        const submitButton = document.getElementById('submit-rating');
        const ratingSuccess = document.getElementById('rating-success');
        let currentRating = parseInt(starsContainer.dataset.userRating) || 0;

        highlightStars(currentRating);
        selectedRating.textContent = currentRating;

        stars.forEach(function (star) {
            star.addEventListener('click', function (_) {
                currentRating = parseInt(this.getAttribute('data-value'));
                selectedRating.textContent = currentRating;
                highlightStars(currentRating);
            });
        });

        function highlightStars(value) {
            stars.forEach(star => {
                const starValue = parseInt(star.getAttribute('data-value'));
                if (starValue <= value) {
                    star.innerHTML = '<i class="fas fa-star" style="color: #ffc107;"></i>';
                } else {
                    star.innerHTML = '<i class="far fa-star" style="color: #e4e5e9;"></i>';
                }
            });
        }

        submitButton.addEventListener('click', function () {
            if (currentRating === 0) {
                alert('Please select a rating first!');
                return;
            }
            submitRatingToDjango(currentRating);
        });

        function submitRatingToDjango(rating) {
            const projectId = document.getElementById('project-id').value;
            const userId = document.getElementById('user-id').value;
            fetch(`/crowdfunding/api/${projectId}/${userId}/rate/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ rating: rating })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        ratingSuccess.style.display = 'block';
                        selectedRating.textContent = data.average_rating;
                        document.getElementById('avg-rating').textContent = data.average_rating;
                        document.getElementById('total-ratings').textContent = data.total_ratings;
                        setTimeout(() => {
                            ratingSuccess.style.display = 'none';
                        }, 3000);
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    }

    // ✅ Tags fetch runs independently (even if no stars exist)
    const projectInput = document.getElementById("project-id");
    if (projectInput) {
        const projectId = projectInput.value;
        console.log("Fetching tags for:", projectId);

        fetch(`/crowdfunding/api/${projectId}/tags/`)
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById("tags-container");
                container.innerHTML = "";
                data.tags.forEach(tag => {
                    const className = `tag-${tag.toLowerCase().replace(/\s+/g, '-')}`;
                    const chip = document.createElement("span");
                    chip.className = `tag ${className}`;
                    chip.innerText = tag;
                    container.appendChild(chip);
                });
            })
            .catch(error => {
                console.error("Error fetching tags:", error);
            });
    }
