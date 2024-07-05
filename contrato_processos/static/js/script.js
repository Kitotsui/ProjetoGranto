document.addEventListener('DOMContentLoaded', function() {
    let uploadArea = document.getElementById('upload-area');
    let fileInput = document.getElementById('file');
    let fileName = document.getElementById('file-name');

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
        fileInput.files = event.dataTransfer.files;
        displayFileName();
    });

    fileInput.addEventListener('change', function() {
        displayFileName();
    });

    function displayFileName() {
        if (fileInput.files.length > 0) {
            fileName.textContent = `Arquivo: ${fileInput.files[0].name}`;
        } else {
            fileName.textContent = '';
        }
    }
});
