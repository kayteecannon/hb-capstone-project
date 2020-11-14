"use strict"

function openItemEditor() {
    window.location.href = "http://localhost:5000/user/1/inventory/item-editor/1"
}

$("#item-1-row").on("click", openItemEditor);