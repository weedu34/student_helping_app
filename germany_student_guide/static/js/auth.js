// static/js/auth.js

// Authentication page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeAuthPage();
});

function initializeAuthPage() {
    setupFormValidation();
    setupPasswordToggle();
    setupFormSubmissionHandling();
    setupFieldDependencies();
}

// Form validation enhancement
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
    });
}

// Validate individual field
function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    const isRequired = field.hasAttribute('required');
    
    // Clear previous validation
    clearFieldValidation(field);
    
    // Required field validation
    if (isRequired && !value) {
        setFieldError(field, 'This field is required');
        return false;
    }
    
    // Email validation
    if (fieldType === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            setFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }
    
    // Password validation
    if (field.name === 'password1' && value) {
        if (value.length < 8) {
            setFieldError(field, 'Password must be at least 8 characters long');
            return false;
        }
    }
    
    // Confirm password validation
    if (field.name === 'password2' && value) {
        const password1 = document.querySelector('input[name="password1"]');
        if (password1 && password1.value !== value) {
            setFieldError(field, 'Passwords do not match');
            return false;
        }
    }
    
    // Phone number validation
    if (field.name === 'phone_number' && value) {
        const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
        if (!phoneRegex.test(value)) {
            setFieldError(field, 'Please enter a valid phone number');
            return false;
        }
    }
    
    // If we get here, field is valid
    setFieldValid(field);
    return true;
}

// Set field error state
function setFieldError(field, message) {
    field.classList.add('is-invalid');
    field.classList.remove('is-valid');
    
    let feedback = field.parentNode.querySelector('.invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentNode.appendChild(feedback);
    }
    feedback.textContent = message;
}

// Set field valid state
function setFieldValid(field) {
    field.classList.add('is-valid');
    field.classList.remove('is-invalid');
    
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.remove();
    }
}

// Clear field validation
function clearFieldValidation(field) {
    field.classList.remove('is-valid', 'is-invalid');
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.remove();
    }
}

// Clear field error on input
function clearFieldError(field) {
    if (field.classList.contains('is-invalid')) {
        field.classList.remove('is-invalid');
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    }
}

// Password visibility toggle
function setupPasswordToggle() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(field => {
        const wrapper = document.createElement('div');
        wrapper.className = 'position-relative';
        
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        
        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.className = 'btn btn-outline-secondary position-absolute end-0 top-50 translate-middle-y';
        toggleButton.style.cssText = 'border: none; background: transparent; z-index: 10; margin-right: 10px;';
        toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
        
        toggleButton.addEventListener('click', function() {
            const isPassword = field.type === 'password';
            field.type = isPassword ? 'text' : 'password';
            this.innerHTML = isPassword ? '<i class="fas fa-eye-slash"></i>' : '<i class="fas fa-eye"></i>';
        });
        
        wrapper.appendChild(toggleButton);
    });
}

// Form submission handling
function setupFormSubmissionHandling() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            let isValid = true;
            
            // Validate all fields
            const fields = form.querySelectorAll('input[required], select[required], textarea[required]');
            fields.forEach(field => {
                if (!validateField(field)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please correct the errors above', 'danger');
                return;
            }
            
            // Add loading state
            if (submitButton) {
                submitButton.classList.add('btn-loading');
                submitButton.disabled = true;
                const originalText = submitButton.textContent;
                submitButton.textContent = 'Processing...';
                
                // Restore button after timeout (fallback)
                setTimeout(() => {
                    submitButton.classList.remove('btn-loading');
                    submitButton.disabled = false;
                    submitButton.textContent = originalText;
                }, 30000);
            }
        });
    });
}

// Setup field dependencies
function setupFieldDependencies() {
    // University field changes
    const universityField = document.querySelector('select[name="university"]');
    if (universityField) {
        universityField.addEventListener('change', function() {
            updateCityOptions(this.value);
        });
    }
    
    // Arrival status changes
    const statusField = document.querySelector('select[name="arrival_status"]');
    if (statusField) {
        statusField.addEventListener('change', function() {
            toggleArrivalFields(this.value);
        });
        
        // Initial call
        toggleArrivalFields(statusField.value);
    }
}

// Update city options based on university
function updateCityOptions(university) {
    const cityField = document.querySelector('input[name="intended_city"]');
    if (!cityField) return;
    
    const citySuggestions = {
        'TU_BERLIN': 'Berlin',
        'LMU_MUNICH': 'Munich',
        'HEIDELBERG': 'Heidelberg',
        'TU_MUNICH': 'Munich',
        'HAMBURG': 'Hamburg',
        'FRANKFURT': 'Frankfurt',
        'COLOGNE': 'Cologne'
    };
    
    if (citySuggestions[university] && !cityField.value) {
        cityField.value = citySuggestions[university];
        cityField.dispatchEvent(new Event('input'));
    }
}

// Toggle arrival-related fields
function toggleArrivalFields(status) {
    const arrivalDateField = document.querySelector('input[name="arrival_date"]');
    const arrivalAirportField = document.querySelector('input[name="arrival_airport"]');
    
    const shouldShow = status === 'PLANNING';
    
    if (arrivalDateField) {
        arrivalDateField.parentNode.style.display = shouldShow ? 'block' : 'none';
        if (shouldShow) {
            arrivalDateField.setAttribute('required', 'required');
        } else {
            arrivalDateField.removeAttribute('required');
        }
    }
    
    if (arrivalAirportField) {
        arrivalAirportField.parentNode.style.display = shouldShow ? 'block' : 'none';
    }
}

// Auto-save form data (optional)
function setupAutoSave() {
    const form = document.querySelector('form');
    if (!form) return;
    
    const formData = {};
    const inputs = form.querySelectorAll('input, select, textarea');
    
    // Load saved data
    const savedData = localStorage.getItem('form_autosave');
    if (savedData) {
        try {
            const parsed = JSON.parse(savedData);
            Object.keys(parsed).forEach(key => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field && field.type !== 'password') {
                    field.value = parsed[key];
                }
            });
        } catch (e) {
            console.log('Could not load saved form data');
        }
    }
    
    // Save data on change
    inputs.forEach(input => {
        if (input.type !== 'password') {
            input.addEventListener('change', function() {
                formData[this.name] = this.value;
                localStorage.setItem('form_autosave', JSON.stringify(formData));
            });
        }
    });
    
    // Clear saved data on successful submission
    form.addEventListener('submit', function() {
        localStorage.removeItem('form_autosave');
    });
}

// Initialize auto-save if needed
// setupAutoSave(); // Uncomment if you want form auto-save functionality