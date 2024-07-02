document.addEventListener('DOMContentLoaded', function() {
    let uploadArea = document.getElementById('upload-area');

    uploadArea.addEventListener('dragover', function(event) {
        event.preventDefault();
        uploadArea.classList.add('dragging');
    });

    uploadArea.addEventListener('dragleave', function(event) {
        event.preventDefault();
        uploadArea.classList.remove('dragging');
    });

    uploadArea.addEventListener('drop', function(event) {
        event.preventDefault();
        uploadArea.classList.remove('dragging');
        let fileInput = document.getElementById('file');
        fileInput.files = event.dataTransfer.files;
    });
});
