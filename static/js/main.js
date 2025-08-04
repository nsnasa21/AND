// Main JavaScript for the news aggregator
document.addEventListener('DOMContentLoaded', function() {
    // Highlight active nav link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Toggle duplicate functionality
    window.toggleDuplicate = function(articleId) {
        fetch(`/toggle-duplicate/${articleId}/`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const btn = document.getElementById(`duplicate-btn-${articleId}`);
                if (data.is_duplicate) {
                    btn.innerHTML = '<i class="bi bi-flag-fill"></i> Marked as Duplicate';
                    btn.classList.remove('btn-outline-warning');
                    btn.classList.add('btn-warning');
                } else {
                    btn.innerHTML = '<i class="bi bi-flag"></i> Mark as Duplicate';
                    btn.classList.remove('btn-warning');
                    btn.classList.add('btn-outline-warning');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };
    
    // Select all checkboxes
    const selectAllCheckbox = document.getElementById('select-all');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('input[name="selected_articles"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
    
    // Date picker initialization
    const today = new Date().toISOString().split('T')[0];
    const dateFromInput = document.getElementById('date_from');
    const dateToInput = document.getElementById('date_to');
    
    if (dateFromInput) {
        dateFromInput.max = today;
    }
    
    if (dateToInput) {
        dateToInput.max = today;
    }
});
