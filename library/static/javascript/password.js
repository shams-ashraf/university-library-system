document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('password-reset-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const csrfToken = formData.get('csrfmiddlewaretoken');
        const url = form.getAttribute('action') || window.location.href;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json',
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            const errorsDiv = document.getElementById('errors');
            errorsDiv.innerHTML = ''; 

            if (data.success) {
                window.location.href = data.redirect_url; 
            } else {
                for (const [field, errors] of Object.entries(data.errors)) {
                    errors.forEach(error => {
                        errorsDiv.innerHTML += `<p>${error}</p>`;
                    });
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
