document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Login successful');
                window.location.href = data.redirect_url;
            } else {
                const errors = JSON.parse(data.errors);
                let errorMessages = 'Your account does not exist:\n\n';
                for (let field in errors) {
                    for (let error of errors[field]) {
                        errorMessages += `${field}: ${error.message}\n`;
                    }
                }
                alert(errorMessages);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Your account does not exist');
        });
    });
});
