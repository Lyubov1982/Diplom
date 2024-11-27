
// static/uikit/like.js
document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const photoId = this.getAttribute('data-photo-id');
            const videoId = this.getAttribute('data-video-id');
            const projectId = this.getAttribute('data-project-id');
            let url;

            if (photoId) {
                url = `/users/like_photo/${photoId}/`;
            } else if (videoId) {
                url = `/users/like_video/${videoId}/`;
            } else if (projectId) {
                url = `/projects/like_project/${projectId}/`;
            } else {
                console.error('No data-id attribute found');
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