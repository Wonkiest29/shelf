async function getItems() {
    const token = localStorage.getItem('token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    const response = await fetch('http://127.0.0.1:8000/items/', {
        method: 'GET',
        headers: headers
    });

    const data = await response.json();
    if (response.ok) {
        if (Array.isArray(data)) {
            const itemsTableBody = document.getElementById('items-table-body');
            itemsTableBody.innerHTML = '';
            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.name}</td>
                    <td>${item.type}</td>
                    <td>${item.description}</td>
                `;
                itemsTableBody.appendChild(row);
            });
        } else {
            console.error('No items found in response:', data);
            alert('No items found.');
        }
    } else if (response.status === 403) {
        alert('Access forbidden. Please login.');
    } else {
        console.error('Failed to fetch items:', data);
        alert('Failed to fetch items: ' + data.message);
    }
}

// Call getItems on page load
window.onload = getItems;