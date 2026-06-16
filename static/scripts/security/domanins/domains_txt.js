const txtFileInput = document.getElementById('txt_file_input')
const domainsTextarea = document.getElementById('domains_textarea')

txtFileInput.addEventListener('change', function() {
    const file = txtFileInput.files[0]
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        domainsTextarea.value = e.target.result;
    }
    reader.readAsText(file);
});