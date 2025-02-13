const fileBtn = document.getElementById('choice-btn-file');
const textBtn = document.getElementById('choice-btn-text');
const uploadBtn = document.getElementById('upload-btn');
const backBtn = document.getElementById('back-btn');

const title = document.getElementById('title');
const description = document.getElementById('description');
const choiceBtnContainer = document.getElementById('choice-btn-container');
const fileInputContainer = document.getElementById('file-input-container');
const textInputContainer = document.getElementById('text-input-container');
const actionBtnContainer = document.getElementById('action-btn-container');

const fileInput = document.getElementById('file-input');
const textInput = document.getElementById('text-input');

fileBtn.addEventListener('click', () => {
    title.textContent = 'Upload a file';
    description.textContent = 'The file must have a function named controller and a reference signal. Name the file your student number. Download the example file.';
    choiceBtnContainer.classList.add('hidden');
    fileInputContainer.classList.remove('hidden');
    actionBtnContainer.classList.remove('hidden');
});
textBtn.addEventListener('click', () => {
    title.textContent = 'Upload your code';
    description.textContent = 'Fill in your controller and reference signal.';
    choiceBtnContainer.classList.add('hidden');
    textInputContainer.classList.remove('hidden');
    actionBtnContainer.classList.remove('hidden');
});
backBtn.addEventListener('click', () => {
    title.textContent = 'Upload your code';
    description.textContent = 'Fill in your controller and reference signal.';
    choiceBtnContainer.classList.remove('hidden');
    fileInputContainer.classList.add('hidden');
    textInputContainer.classList.add('hidden');
    actionBtnContainer.classList.add('hidden');
});
uploadBtn.addEventListener('click', async() => {
    const authResponse = await fetch('/get_auth_state');
    const authResult = await authResponse.json();
    if (authResult.is_logged_in){
        const stuNumber = ('; '+document.cookie).split(`; stu_number=`).pop().split(';')[0];
        if(!fileInputContainer.classList.contains('hidden')){ //if the file container is NOT hidden
            //you upload the file
            const file = fileInput.files[0];
            if(!file){
                alert('Please choose a file');
                return;
            }
            const formData = new FormData();
            formData.append('file', file);
            formData.append('stu_number', stuNumber);

            const response = await fetch(`/upload_file/${stuNumber}`, {
                method: 'POST',
                body: formData
            })
            const result = await response.json();
            alert(result.message);
        } else { //if file container is hidden
            //you upload the text
            const textData = textInput.value;
            if(!textData){
                alert("Text area is empty");
                return;
            }
            const response = await fetch(`/upload_text/${stuNumber}`, {
                method: 'POST',
                headers: {'Content-type':'application/json'},
                body: JSON.stringify({text: textData})
            })
            const result = await response.json();
            alert(result.message);
        }
    } else {
        alert('Please login')
    }
})