const authContainer = document.getElementById("auth-container");
async function fetchAuthState() {
    try {
        const response = await fetch('/get_auth_state');
        const data = await response.json();
        // Clear previous content in auth container
        authContainer.innerHTML = '';
        if (data.is_logged_in) {
            const logoutBtn = document.createElement('button');
            logoutBtn.id = 'logout-btn';
            logoutBtn.textContent = 'Logout';
            logoutBtn.addEventListener('click', logout);
            authContainer.appendChild(logoutBtn);
        } else {
            // If not logged in, show login form
            const loginForm = document.createElement('form');
            loginForm.id = 'login-form';
            loginForm.action = '/login';
            loginForm.method = 'POST';
            const emailInput = document.createElement('input');
            emailInput.type = 'email';
            emailInput.name = 'email';
            emailInput.placeholder = 'email';
            const numberInput = document.createElement('input');
            numberInput.type = 'text';
            numberInput.name = 'stu_number';
            numberInput.placeholder = 'number';
            const submitButton = document.createElement('button');
            submitButton.type = 'submit';
            submitButton.textContent = 'Login';
            loginForm.appendChild(emailInput);
            loginForm.appendChild(numberInput);
            loginForm.appendChild(submitButton);
            loginForm.addEventListener('submit', login);
            authContainer.appendChild(loginForm);
        }
    } catch (error) {
        console.error('Error fetching auth state:', error);
    }
}
async function login(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    try {
        const response = await fetch('/login', {
            method: 'POST',
            body: formData,
            credentials: 'same-origin'
        });
        const result = await response.json();
        if (result.success) {
            fetchAuthState(); // Update UI
            fetchTable(); // Update table if needed
        } else {
            alert('Login failed. Please check your email and student number.');
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
}
// Handle logout
async function logout() {
    try {
        const response = await fetch('/logout', {
            method: 'POST',
            credentials: 'same-origin'
        });
        if (response.ok) {
            fetchAuthState(); // Update UI
            fetchTable(); // Update table if needed
            clearCookies();
        }
    } catch (error) {
        console.error('Error during logout:', error);
    }
}
function clearCookies() {
    document.cookie = "email=; expires= Tue, 11 Sep 2001 13:14:00 GMT+1, path=/;";
    location.reload();
}
async function fetchTable() {
    try{
        const response = await fetch('get_table');
        const data = await response.json();
        const table = document.getElementById('number-email').querySelector('tbody');
        table.innerHTML = '';
        for (const [key, value] of Object.entries(data)){
            const row = document.createElement('tr');
            const keyCell = document.createElement('td');
            const valueCell = document.createElement('td');
            keyCell.textContent = key;
            valueCell.textContent = value;
            row.appendChild(keyCell);
            row.appendChild(valueCell);
            table.appendChild(row);
        }
    } catch(error){
        console.error('Error getting logged in table:', error)
    }
}
window.onload = () => {
    fetchAuthState();
    fetchTable();
}