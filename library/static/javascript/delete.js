document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('delete-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const csrfToken = formData.get('csrfmiddlewaretoken');
        const url = form.getAttribute('action') || window.location.href;

        if (confirm('Are you sure you want to delete this book?')) {
            formData.set('confirm_delete', 'true');  
            
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
                    alert('Book deleted successfully.');
                    window.location.href = '/avaliable/';  
                } else {
                    alert('Failed to delete book. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the book.');
            });
        }
    });
});
