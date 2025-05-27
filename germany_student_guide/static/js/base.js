// static/js/base.js

// Base JavaScript functionality for the entire application
document.addEventListener('DOMContentLoaded', function() {
    initializeBaseFeatures();
});

// Initialize base features
function initializeBaseFeatures() {
    setupAlertAutoHide();
    setupFormEnhancements();
    setupGlobalUtilities();
}

// Auto-hide dismissible alerts after 5 seconds
function setupAlertAutoHide() {
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert.alert-dismissible');
        alerts.forEach(function(alert) {
            if (bootstrap && bootstrap.Alert) {
                try {
                    let bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } catch (error) {
                    console.log('Alert already closed or invalid');
                }
            }
        });
    }, 5000);
}

// Setup form enhancements
function setupFormEnhancements() {
    // Add loading states to form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                }, 10000);
            }
        });
    });

    // Add focus styles to form inputs
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

// Setup global utilities
function setupGlobalUtilities() {
    // Add smooth scrolling to all anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add hover effects to cards
    const cards = document.querySelectorAll('.card, .auth-card, .bg-white');
    cards.forEach(card => {
        if (!card.classList.contains('no-hover')) {
            card.classList.add('card-hover');
        }
    });
}

// Global notification system
function showNotification(message, type = 'success', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 400px;
    `;
    
    const iconMap = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    
    notification.innerHTML = `
        <i class="fas fa-${iconMap[type] || 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-hide after specified duration
    setTimeout(() => {
        if (notification.parentNode) {
            const bsAlert = new bootstrap.Alert(notification);
            bsAlert.close();
        }
    }, duration);
    
    return notification;
}

// Loading overlay utility
function showLoadingOverlay(message = 'Loading...') {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
    overlay.style.cssText = `
        background: rgba(0, 0, 0, 0.7);
        z-index: 9999;
        backdrop-filter: blur(5px);
    `;
    
    overlay.innerHTML = `
        <div class="text-center text-white">
            <div class="spinner-border mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div>${message}</div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    return overlay;
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Confirm dialog utility
function showConfirmDialog(message, onConfirm, onCancel = null) {
    const confirmed = confirm(message);
    if (confirmed && onConfirm) {
        onConfirm();
    } else if (!confirmed && onCancel) {
        onCancel();
    }
    return confirmed;
}

// Copy to clipboard utility
function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification(successMessage, 'success', 2000);
        }).catch(() => {
            fallbackCopyToClipboard(text, successMessage);
        });
    } else {
        fallbackCopyToClipboard(text, successMessage);
    }
}

function fallbackCopyToClipboard(text, successMessage) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showNotification(successMessage, 'success', 2000);
    } catch (err) {
        showNotification('Failed to copy to clipboard', 'danger', 3000);
    }
    
    textArea.remove();
}

// Export global utilities
window.showNotification = showNotification;
window.showLoadingOverlay = showLoadingOverlay;
window.hideLoadingOverlay = hideLoadingOverlay;
window.showConfirmDialog = showConfirmDialog;
window.copyToClipboard = copyToClipboard;