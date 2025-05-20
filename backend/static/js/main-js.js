// Main JavaScript file for Hospital Website

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const navToggle = document.querySelector('.nav-toggle');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            const nav = document.querySelector('nav ul');
            nav.classList.toggle('show');
        });
    }
    
    // Form validation for appointment form
    const appointmentForm = document.querySelector('form[action*="appointment"]');
    
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', function(e) {
            const nameField = document.getElementById('name');
            const emailField = document.getElementById('email');
            const dateField = document.getElementById('date');
            const timeField = document.getElementById('time');
            
            let isValid = true;
            
            // Simple validation
            if (nameField && nameField.value.trim() === '') {
                isValid = false;
                showError(nameField, 'Please enter your name');
            }
            
            if (emailField && !isValidEmail(emailField.value)) {
                isValid = false;
                showError(emailField, 'Please enter a valid email address');
            }
            
            if (dateField && !isValidDate(dateField.value)) {
                isValid = false;
                showError(dateField, 'Please select a valid date');
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // Helper functions
    function showError(field, message) {
        // Remove any existing error messages
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error class to the field
        field.classList.add('error');
        
        // Create and append error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }
    
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
    
    function isValidDate(date) {
        const selectedDate = new Date(date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        return selectedDate instanceof Date && !isNaN(selectedDate) && selectedDate >= today;
    }
});
