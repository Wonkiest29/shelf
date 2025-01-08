document.getElementById('signin-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        alert('Please enter both username and password.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/signin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('token', data.token);
            window.location.href = '/';
        } else {
            alert('Login failed: ' + data.detail);
        }
    } catch (error) {
        console.error('Error during sign-in:', error);
        alert('An error occurred during sign-in. Please try again later.');
    }
});