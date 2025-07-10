document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('edit-book-form');
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
                alert('Book edited successfully');
                window.location.href = data.redirect_url;
            } else {
                let alertMessage = '';
                if (data.message) {
                    alertMessage = data.message;
                } else if (data.errors) {
                    for (const [field, errors] of Object.entries(data.errors)) {
                        errors.forEach(error => {
                            alertMessage += `${field}: ${error}\n`;
                        });
                    }
                } else {
                    alertMessage = 'An error occurred while editing the book.';
                }
                alert(alertMessage);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
