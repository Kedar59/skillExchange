document.addEventListener('DOMContentLoaded', function () {

    const updateFirstNameButton = document.getElementById('update-first-name-button');
    const updateFirstNameForm = document.getElementById('update-first-name-form');

    updateFirstNameButton.addEventListener('click', function () {
        updateFirstNameForm.style.display = 'block';
        updateFirstNameButton.style.display = 'none';
    });

    const updateLastNameButton = document.getElementById('update-last-name-button');
    const updateLastNameForm = document.getElementById('update-last-name-form');

    updateLastNameButton.addEventListener('click', function () {
        updateLastNameForm.style.display = 'block';
        updateLastNameButton.style.display = 'none';
    });

    const updateUserBioButton = document.getElementById('update-userBio-button');
    const updateUserBioForm = document.getElementById('update-userBio-form');

    updateUserBioButton.addEventListener('click', function () {
        updateUserBioForm.style.display = 'block';
        updateUserBioButton.style.display = 'none';
    });

    const updateProfPicButton = document.getElementById('update-prof-pic-button');
    const updateProfPicForm = document.getElementById('update-prof-pic-form');

    updateProfPicButton.addEventListener('click', function () {
        updateProfPicForm.style.display = 'block';
        updateProfPicButton.style.display = 'none';
    });
});