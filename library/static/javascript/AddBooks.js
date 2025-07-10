document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('add');
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
            if (data.success) {
                alert('Book added successfully');
                window.location.href = data.redirect_url;
            } else {
                let alertMessage = '';
                for (const [field, errors] of Object.entries(data.errors)) {
                    errors.forEach(error => {
                        alertMessage += `${field}: ${error}\n`;
                    });
                }
                alert(alertMessage);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
