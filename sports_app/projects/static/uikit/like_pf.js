document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const itemId = this.getAttribute('data-item-id');
            const itemType = this.getAttribute('data-item-type');
            let url;

            if (itemType === 'photo') {
                url = `/users/like_photo/${itemId}/`;
            } else if (itemType === 'video') {
                url = `/users/like_video/${itemId}/`;
            } else {
                console.error('No data-item-type attribute found');
                return;
            }

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                const likeCount = this.querySelector('.like-count');
                if (likeCount) {
                    likeCount.textContent = data.likes_count;
                } else {
                    console.error('No like-count element found');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});