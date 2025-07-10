document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('borrow');

    if (!form) {
        console.error("Form with id 'borrow' not found!");
        return;
    }

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
                alert('Book borrowed successfully!');
                window.location.href = data.redirect_url;
            } else {
                if (data.message) {
                    alert(data.message); 
                } else {
                    let alertMessage = '';
                    if (data.alertMessage) {
                        alertMessage += data.alertMessage + '\n';
                    }
                    for (const [field, errors] of Object.entries(data.errors || {})) {
                        errors.forEach(error => {
                            alertMessage += `${field}: ${error}\n`;
                        });
                    }
                    alert(alertMessage);
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
