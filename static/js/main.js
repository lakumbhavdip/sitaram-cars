// Sitaram Cars Javascript Helpers

document.addEventListener('DOMContentLoaded', function() {
    // Image Preview helper for file inputs
    const mainImageInput = document.getElementById('main_image');
    const mainImagePreview = document.getElementById('main_image_preview');

    if (mainImageInput && mainImagePreview) {
        mainImageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(evt) {
                    mainImagePreview.src = evt.target.result;
                    mainImagePreview.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Multiple Images Preview helper
    const multiImagesInput = document.getElementById('images');
    const multiImagesContainer = document.getElementById('gallery_previews');

    if (multiImagesInput && multiImagesContainer) {
        multiImagesInput.addEventListener('change', function(e) {
            multiImagesContainer.innerHTML = '';
            const files = Array.from(e.target.files);
            files.forEach((file, idx) => {
                const reader = new FileReader();
                reader.onload = function(evt) {
                    const col = document.createElement('div');
                    col.className = 'col-3 position-relative mb-2';
                    col.innerHTML = `
                        <img src="${evt.target.result}" class="img-thumbnail" style="height: 90px; width: 100%; object-fit: cover;">
                        <span class="badge bg-dark position-absolute top-0 start-0 m-1">${idx + 1}</span>
                    `;
                    multiImagesContainer.appendChild(col);
                };
                reader.readAsDataURL(file);
            });
        });
    }
});

// Switch Main Image on Car Detail Gallery
function setMainGalleryImage(src) {
    const mainImg = document.getElementById('carMainGalleryDisplay');
    if (mainImg) {
        mainImg.src = src;
    }
}
