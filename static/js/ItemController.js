"use strict"

function makeItemsClickable(response) {

    const itemIDs = [];
    for (const [key, value] of Object.entries(response)) {
        itemIDs.push(value);
      }

    for (const id of itemIDs) {
        $(`#item-${id}-row`).on("click", () => {
            window.location.href = `http://localhost:5000/user/1/inventory/item-editor/${id}`;
        });
    }
    
}

$.get('/get-item-ids', makeItemsClickable);