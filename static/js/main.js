// Modern JavaScript for CubeManager

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initializeMessages();
    initializeBulkOperations();
    initializeFormValidation();
    initializeAnimations();
});

// Message management
function initializeMessages() {
    const messages = document.querySelectorAll('.message');
    
    // Auto-hide success messages after 5 seconds
    messages.forEach(message => {
        if (message.classList.contains('message-success')) {
            setTimeout(() => {
                message.style.opacity = '0';
                message.style.transform = 'translateY(-10px)';
                setTimeout(() => message.remove(), 300);
            }, 5000);
        }
    });
}

// Bulk operations for tree management
function initializeBulkOperations() {
    // Only run if we're on the bulk update page
    if (!document.querySelector('.bulk-update-form')) return;
    
    // Initialize bulk selection functionality
    setupBulkSelection();
}

function setupBulkSelection() {
    const selectAllBtn = document.querySelector('[onclick="selectAllTrees()"]');
    const deselectAllBtn = document.querySelector('[onclick="deselectAllTrees()"]');
    const bulkStatusSelect = document.getElementById('bulk-status');
    const applyBtn = document.querySelector('[onclick="applyBulkStatus()"]');
    
    if (selectAllBtn) {
        selectAllBtn.onclick = selectAllTrees;
    }
    
    if (deselectAllBtn) {
        deselectAllBtn.onclick = deselectAllTrees;
    }
    
    if (applyBtn) {
        applyBtn.onclick = applyBulkStatus;
    }
}

// Bulk selection functions
function selectAllTrees() {
    const checkboxes = document.querySelectorAll('.tree-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = true;
        highlightSelectedTree(checkbox, true);
    });
    updateBulkButtonState();
}

function deselectAllTrees() {
    const checkboxes = document.querySelectorAll('.tree-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
        highlightSelectedTree(checkbox, false);
    });
    updateBulkButtonState();
}

function applyBulkStatus() {
    const bulkStatus = document.getElementById('bulk-status').value;
    const selectedCheckboxes = document.querySelectorAll('.tree-checkbox:checked');
    
    if (!bulkStatus) {
        showTemporaryMessage('Please select a status to apply', 'warning');
        return;
    }
    
    if (selectedCheckboxes.length === 0) {
        showTemporaryMessage('Please select at least one tree', 'warning');
        return;
    }
    
    // Apply status to selected trees
    selectedCheckboxes.forEach(checkbox => {
        const treeId = checkbox.dataset.treeId;
        const statusSelect = document.getElementById(`status_${treeId}`);
        if (statusSelect) {
            statusSelect.value = bulkStatus;
            
            // Visual feedback
            const card = checkbox.closest('.tree-bulk-card');
            card.style.transform = 'scale(0.98)';
            setTimeout(() => {
                card.style.transform = 'scale(1)';
            }, 150);
        }
    });
    
    showTemporaryMessage(`Status applied to ${selectedCheckboxes.length} tree(s)`, 'success');
    
    // Reset bulk selector
    document.getElementById('bulk-status').value = '';
}

function highlightSelectedTree(checkbox, selected) {
    const card = checkbox.closest('.tree-bulk-card');
    if (selected) {
        card.style.borderColor = 'var(--accent-primary)';
        card.style.background = 'linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary))';
    } else {
        card.style.borderColor = 'var(--border-color)';
        card.style.background = 'var(--bg-secondary)';
    }
}

function updateBulkButtonState() {
    const selectedCount = document.querySelectorAll('.tree-checkbox:checked').length;
    const applyBtn = document.querySelector('[onclick="applyBulkStatus()"]');
    
    if (applyBtn) {
        if (selectedCount > 0) {
            applyBtn.textContent = `Apply to ${selectedCount} tree${selectedCount !== 1 ? 's' : ''}`;
            applyBtn.disabled = false;
        } else {
            applyBtn.textContent = 'Apply';
            applyBtn.disabled = true;
        }
    }
}

// Form validation and enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Add loading state to submit buttons
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitBtn.textContent = 'Processing...';
                submitBtn.disabled = true;
                
                // Re-enable if form validation fails
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.textContent = originalText;
                        submitBtn.disabled = false;
                    }
                }, 5000);
            }
        });
        
        // Enhanced number input validation
        const numberInputs = form.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.addEventListener('input', function() {
                const value = parseInt(this.value);
                const min = parseInt(this.getAttribute('min')) || 0;
                
                if (value < min) {
                    this.setCustomValidity(`Value must be at least ${min}`);
                } else {
                    this.setCustomValidity('');
                }
            });
        });
    });
}

// Animation and interaction enhancements
function initializeAnimations() {
    // Add intersection observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe cards for animation
    const cards = document.querySelectorAll('.cube-card, .tree-card, .detail-card, .tree-list-item');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        card.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Add click ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', createRippleEffect);
    });
    
    // Add tree checkbox event listeners
    const treeCheckboxes = document.querySelectorAll('.tree-checkbox');
    treeCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            highlightSelectedTree(this, this.checked);
            updateBulkButtonState();
        });
    });
}

function createRippleEffect(e) {
    const button = e.currentTarget;
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    const ripple = document.createElement('span');
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        pointer-events: none;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        z-index: 1;
    `;
    
    // Add ripple animation CSS if not already added
    if (!document.getElementById('ripple-styles')) {
        const style = document.createElement('style');
        style.id = 'ripple-styles';
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
            .btn {
                position: relative;
                overflow: hidden;
            }
        `;
        document.head.appendChild(style);
    }
    
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Utility function to show temporary messages
function showTemporaryMessage(text, type = 'info') {
    const messagesContainer = document.querySelector('.messages-container') || 
                             document.querySelector('.main-content');
    
    const message = document.createElement('div');
    message.className = `message message-${type}`;
    message.innerHTML = `
        <span class="message-text">${text}</span>
        <button class="message-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    messagesContainer.insertBefore(message, messagesContainer.firstChild);
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-10px)';
        setTimeout(() => message.remove(), 300);
    }, 3000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N for new cube (only on home page)
    if ((e.ctrlKey || e.metaKey) && e.key === 'n' && window.location.pathname === '/') {
        e.preventDefault();
        window.location.href = '/cube/create/';
    }
    
    // Escape to go back or cancel
    if (e.key === 'Escape') {
        const cancelBtn = document.querySelector('.btn-secondary[href*="back"], .btn-secondary[href*="cancel"]');
        if (cancelBtn) {
            cancelBtn.click();
        }
    }
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        if (loadTime > 2000) {
            console.warn('Page load time is slow:', loadTime + 'ms');
        }
    });
}

// Dark theme detection and enhancement
function enhanceDarkTheme() {
    // Add theme-color meta tag for mobile browsers
    const themeColorMeta = document.createElement('meta');
    themeColorMeta.name = 'theme-color';
    themeColorMeta.content = '#0a0a0a';
    document.head.appendChild(themeColorMeta);
    
    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
}

// Initialize theme enhancements
enhanceDarkTheme();

// Export functions for global use
window.CubeManager = {
    selectAllTrees,
    deselectAllTrees,
    applyBulkStatus,
    showTemporaryMessage
};
