// ================================================
// AJAX PARA LIKES E FOLLOWS - CLONE X
// ================================================

document.addEventListener('DOMContentLoaded', function() {
    // Likes
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const form = this;
            const button = form.querySelector('.like-btn');
            const countSpan = form.querySelector('.like-count');

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new FormData(form)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    countSpan.textContent = data.likes_count;
                    if (data.liked) {
                        button.classList.remove('btn-outline-secondary');
                        button.classList.add('btn-danger');
                    } else {
                        button.classList.remove('btn-danger');
                        button.classList.add('btn-outline-secondary');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback: submit normal do formulário
                form.submit();
            });
        });
    });

    // Follow/Unfollow
    document.querySelectorAll('.follow-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const form = this;
            const button = form.querySelector('.follow-btn');

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new FormData(form)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.following) {
                        if (button.querySelector('span.d-none')) {
                            button.innerHTML = '<span class="d-none d-md-inline">Deixar</span><span class="d-md-none">❌</span>';
                        } else {
                            button.textContent = 'Deixar de Seguir';
                        }
                        button.classList.remove('btn-dark');
                        button.classList.add('btn-outline-danger');
                    } else {
                        if (button.querySelector('span.d-none')) {
                            button.innerHTML = '<span class="d-none d-md-inline">Seguir</span><span class="d-md-none">➕</span>';
                        } else {
                            button.textContent = 'Seguir';
                        }
                        button.classList.remove('btn-outline-danger');
                        button.classList.add('btn-dark');
                    }

                    // Atualiza contadores de seguidores
                    const followersCount = document.querySelector('.followers-count');
                    if (followersCount && data.followers_count !== undefined) {
                        followersCount.textContent = data.followers_count;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback: submit normal do formulário
                form.submit();
            });
        });
    });
});
