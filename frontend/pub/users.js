document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
    document.getElementById('save-user-button').addEventListener('click', saveUser);
    document.getElementById('cancel-user-button').addEventListener('click', closeModal);
    document.getElementById('close-modal-button').addEventListener('click', closeModal);
});

async function loadUsers() {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch('http://127.0.0.1:8000/users/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            showToast(errorData.error, 'is-danger');
            return;
        }

        const data = await response.json();
        const usersTableBody = document.getElementById('users-table-body');
        usersTableBody.innerHTML = '';
        data.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user._id}</td>
                <td>${user.username}</td>
                <td>${user.role}</td>
                <td>
                    <button class="button is-small is-info" onclick='openEditModal(${JSON.stringify(user)})'>Update</button>
                    <button class="button is-small is-danger" onclick='deleteUser("${user._id}")'>Delete</button>
                </td>
            `;
            usersTableBody.appendChild(row);
        });
    } catch (error) {
        showToast('An error occurred while loading users', 'is-danger');
    }
}

function showToast(message, type = 'is-danger') {
    bulmaToast.toast({
        message: message,
        type: type,
        dismissible: true,
        pauseOnHover: true,
        duration: 3000,
        position: 'top-right'
    });
}

function openEditModal(user) {
    const modal = document.getElementById('edit-user-modal');
    modal.classList.add('is-active');
    document.getElementById('edit-username').value = user.username;
    document.getElementById('edit-role').value = user.role;
    document.getElementById('edit-password').value = ''; // Clear the password field
    currentUser = user; // Store the current user being edited
}

function closeModal() {
    const modal = document.getElementById('edit-user-modal');
    modal.classList.remove('is-active');
}

async function saveUser() {
    const token = localStorage.getItem('token');
    const username = document.getElementById('edit-username').value;
    const role = document.getElementById('edit-role').value;
    const password = document.getElementById('edit-password').value;

    const response = await fetch(`http://127.0.0.1:8000/users/${currentUser._id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ username, role, password })
    });

    if (response.ok) {
        closeModal();
        loadUsers();
    } else {
        const errorData = await response.json();
        console.error('Failed to save user:', errorData);
        alert('Failed to save user');
    }
}

async function deleteUser(id) {
    const token = localStorage.getItem('token');
    const response = await fetch(`http://127.0.0.1:8000/users/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        loadUsers();
    } else {
        const errorData = await response.json();
        console.error('Failed to delete user:', errorData);
        alert('Failed to delete user');
    }
}