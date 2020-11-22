"use strict"

const deleteButton = $('#delete-item');

const itemName = $('#item-name').val();
const itemQuantity = $('#item-quantity').val();
const itemExpiration = $('#item-expiration').val();

const itemDict = {name: itemName, quantity: itemQuantity, expiration: itemExpiration};

function confirmDelete() {

    if (confirm("Are you sure you want to delete?")) {

        //alert(`${JSON.stringify(itemDict)}`);
      $.ajax({
        type : "POST",
        url : '/delete-item',
        dataType: "json",
        data: JSON.stringify(itemDict),
        contentType: 'application/json;charset=UTF-8',
        success: function (data) {
            console.log('SUCCESS', data);
            window.location.href = "/user/1/inventory";
            },
        error: function (data) {
            console.log('ERROR', data);
        }
        });
  }
}

deleteButton.on('click', () => {
  confirmDelete();
});