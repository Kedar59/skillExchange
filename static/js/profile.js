document.addEventListener('DOMContentLoaded', function () {
    const updateFirstNameButton = document.getElementById('update-first-name-button');
    const updateFirstNameForm = document.getElementById('update-first-name-form');

    updateFirstNameButton.addEventListener('click', function () {
        updateFirstNameForm.style.display = 'block';
        updateFirstNameButton.style.display = 'none';
    });
});