"use strict"

const deleteButton = $('#delete-item');

function confirmDelete() {

    if (confirm("Are you sure you want to delete?")) {
      alert("Item deleted!")
  }
}

deleteButton.on('click', () => {
  confirmDelete();
});