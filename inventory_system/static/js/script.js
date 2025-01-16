// Example: Add some interactivity for form submission feedback
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            alert('Form submitted successfully!');
        });
    });
});
