"use strict"

function makeItemsClickable(response) {

    const itemIDs = [];
    for (const [key, value] of Object.entries(response['items'])) {
        itemIDs.push(value);
      }

    for (const id of itemIDs) {
        $(`#item-${id}-row`).on("click", () => {
            window.location.href = `http://localhost:5000/user/${response['user_id']}/inventory/item-editor/${id}`;
        });
    }
    
}

// On load, add event listener to all item rows
$.get('/get-item-ids', makeItemsClickable);