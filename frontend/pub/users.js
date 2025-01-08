document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
});

async function loadUsers() {
    const token = localStorage.getItem('token');
    const response = await fetch('http://127.0.0.1:8000/users/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
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
}

async function saveUser() {
    const token = localStorage.getItem('token');
    const username = document.getElementById('user-username').value;
    const role = document.getElementById('user-role').value;

    const response = await fetch(`http://127.0.0.1:8000/users/${currentUser._id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ username, role })
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
    const response = await fetch(`http://127.0.0.1:8000/user/${id}`, {
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