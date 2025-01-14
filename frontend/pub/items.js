let currentItem = null;

document.addEventListener('DOMContentLoaded', () => {
    loadItems();
});

function openCreateModal() {
    currentItem = null;
    document.getElementById('modal-title').innerText = 'Create Item';
    document.getElementById('item-form').reset();
    document.getElementById('item-modal').classList.add('is-active');
}

function openEditModal(item) {
    currentItem = item;
    document.getElementById('modal-title').innerText = 'Edit Item';
    document.getElementById('item-name').value = item.name;
    document.getElementById('item-type').value = item.type;
    document.getElementById('item-description').value = item.description;
    document.getElementById('item-modal').classList.add('is-active');
}

function closeModal() {
    document.getElementById('item-modal').classList.remove('is-active');
}

async function loadItems() {
    const response = await fetch('/api/items/');
    const data = await response.json();
    const itemsTableBody = document.getElementById('items-table-body');
    itemsTableBody.innerHTML = '';
    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.type}</td>
            <td>${item.description}</td>
            <td>
                <button class="button is-small is-info" onclick='openEditModal(${JSON.stringify(item)})'>Edit</button>
                <button class="button is-small is-danger" onclick='deleteItem("${item.id}")'>Delete</button>
            </td>
        `;
        itemsTableBody.appendChild(row);
    });
}

async function saveItem() {
    const name = document.getElementById('item-name').value;
    const type = document.getElementById('item-type').value;
    const description = document.getElementById('item-description').value;

    const method = currentItem ? 'PUT' : 'POST';
    const url = currentItem ? `http://192.168.1.42:8000/items/${currentItem.id}` : 'http://192.168.1.42:8000/items/';

    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, type, description })
    });

    if (response.ok) {
        closeModal();
        loadItems();
    } else {
        alert('Failed to save item');
    }
}

async function deleteItem(id) {
    const response = await fetch(`/api/items/${id}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        loadItems();
    } else {
        alert('Failed to delete item');
    }
}