// Global utility functions
function showToast(message, type = 'success') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toast = toastContainer.lastElementChild;
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    setTimeout(() => toast.remove(), 5000);
}

// Scan music folder
async function scanMusicFolder() {
    try {
        const response = await axios.get('/api/music/scan');
        showToast(response.data.message, 'success');
        if (window.loadMusicList) {
            window.loadMusicList();
        }
    } catch (error) {
        showToast('Failed to scan music folder', 'danger');
        console.error('Scan error:', error);
    }
}

// Export evaluation data
async function exportData() {
    try {
        const response = await axios.get('/api/export/evaluations');
        const dataStr = JSON.stringify(response.data, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `music_evaluations_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        showToast('Evaluations exported successfully', 'success');
    } catch (error) {
        showToast('Failed to export evaluations', 'danger');
        console.error('Export error:', error);
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Create rating stars display
function createRatingStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
            stars += '<i class="bi bi-star-fill"></i>';
        } else {
            stars += '<i class="bi bi-star"></i>';
        }
    }
    return stars;
}

// Handle rating input interactions
function setupRatingInputs() {
    document.querySelectorAll('.rating-group').forEach(group => {
        const inputs = group.querySelectorAll('input[type="radio"]');
        const stars = group.querySelectorAll('.star-label');
        
        inputs.forEach((input, index) => {
            input.addEventListener('change', () => {
                stars.forEach((star, starIndex) => {
                    if (starIndex <= index) {
                        star.classList.add('text-warning');
                        star.classList.remove('text-muted');
                    } else {
                        star.classList.remove('text-warning');
                        star.classList.add('text-muted');
                    }
                });
            });
        });
        
        stars.forEach((star, starIndex) => {
            star.addEventListener('click', () => {
                inputs[starIndex].click();
            });
            
            star.addEventListener('mouseenter', () => {
                stars.forEach((s, idx) => {
                    if (idx <= starIndex) {
                        s.classList.add('text-warning');
                        s.classList.remove('text-muted');
                    } else {
                        s.classList.remove('text-warning');
                        s.classList.add('text-muted');
                    }
                });
            });
        });
        
        group.addEventListener('mouseleave', () => {
            const checkedInput = group.querySelector('input:checked');
            if (checkedInput) {
                const checkedIndex = Array.from(inputs).indexOf(checkedInput);
                stars.forEach((star, idx) => {
                    if (idx <= checkedIndex) {
                        star.classList.add('text-warning');
                        star.classList.remove('text-muted');
                    } else {
                        star.classList.remove('text-warning');
                        star.classList.add('text-muted');
                    }
                });
            } else {
                stars.forEach(star => {
                    star.classList.remove('text-warning');
                    star.classList.add('text-muted');
                });
            }
        });
    });
}