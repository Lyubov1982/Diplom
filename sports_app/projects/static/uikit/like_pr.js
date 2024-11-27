document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const likeButtons = document.querySelectorAll('.like-button[data-project-id]');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const projectId = this.getAttribute('data-project-id');
            let url = `/projects/like_project/${projectId}/`;

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