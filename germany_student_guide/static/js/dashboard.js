// static/js/dashboard.js

// Initialize dashboard functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

// Main dashboard initialization function
function initializeDashboard() {
    // Prevent the base template's auto-hide alerts from affecting next steps
    setupAlertAutoHide();
    
    // Initialize progress bar animation
    animateProgressBar();
    
    // Setup quick links hover effects
    setupQuickLinksEffects();
}

// Setup alert auto-hide to only target dismissible alerts
function setupAlertAutoHide() {
    setTimeout(function() {
        // Only hide alerts that are NOT in the next steps section
        let alerts = document.querySelectorAll('.alert.alert-dismissible');
        alerts.forEach(function(alert) {
            if (bootstrap && bootstrap.Alert) {
                let bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);
}

// Animate progress bar on page load
function animateProgressBar() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
}

// Setup hover effects for quick links
function setupQuickLinksEffects() {
    const quickLinks = document.querySelectorAll('.d-grid .btn');
    quickLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Function to mark steps as complete
function markStepComplete(button) {
    const stepCard = button.closest('.step-card');
    const icon = button.querySelector('i');
    
    if (stepCard.classList.contains('completed')) {
        // Uncomplete the step
        uncompleteStep(stepCard, button, icon);
    } else {
        // Complete the step
        completeStep(stepCard, button, icon);
    }
}

// Complete a step
function completeStep(stepCard, button, icon) {
    stepCard.classList.add('completed');
    icon.className = 'fas fa-check-circle';
    button.classList.remove('btn-outline-success');
    button.classList.add('btn-success');
    button.title = 'Mark as incomplete';
    
    // Add completion effect
    showCompletionEffect(stepCard);
    
    // Optional: Save completion status to localStorage
    saveStepCompletion(stepCard, true);
}

// Uncomplete a step
function uncompleteStep(stepCard, button, icon) {
    stepCard.classList.remove('completed');
    icon.className = 'fas fa-check';
    button.classList.remove('btn-success');
    button.classList.add('btn-outline-success');
    button.title = 'Mark as complete';
    
    // Optional: Save completion status to localStorage
    saveStepCompletion(stepCard, false);
}

// Show completion effect animation
function showCompletionEffect(stepCard) {
    const completionEffect = document.createElement('div');
    completionEffect.innerHTML = '<i class="fas fa-check-circle text-success fa-2x"></i>';
    completionEffect.className = 'completion-effect';
    
    stepCard.style.position = 'relative';
    stepCard.appendChild(completionEffect);
    
    setTimeout(() => {
        if (completionEffect.parentNode) {
            completionEffect.remove();
        }
    }, 600);
}

// Save step completion status (optional - for persistence)
function saveStepCompletion(stepCard, isCompleted) {
    const stepTitle = stepCard.querySelector('.step-title').textContent.trim();
    const completedSteps = JSON.parse(localStorage.getItem('completedSteps') || '[]');
    
    if (isCompleted && !completedSteps.includes(stepTitle)) {
        completedSteps.push(stepTitle);
    } else if (!isCompleted) {
        const index = completedSteps.indexOf(stepTitle);
        if (index > -1) {
            completedSteps.splice(index, 1);
        }
    }
    
    localStorage.setItem('completedSteps', JSON.stringify(completedSteps));
}

// Load saved step completions on page load
function loadSavedStepCompletions() {
    const completedSteps = JSON.parse(localStorage.getItem('completedSteps') || '[]');
    
    document.querySelectorAll('.step-card').forEach(stepCard => {
        const stepTitle = stepCard.querySelector('.step-title').textContent.trim();
        const button = stepCard.querySelector('.mark-complete-btn');
        
        if (completedSteps.includes(stepTitle) && button) {
            markStepComplete(button);
        }
    });
}

// Load saved completions when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(loadSavedStepCompletions, 100);
});

// Utility function to show custom notifications
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Export functions for global use if needed
window.markStepComplete = markStepComplete;
window.showNotification = showNotification;