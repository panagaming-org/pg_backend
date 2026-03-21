var socket = io()

document.getElementById('delete_image_button').addEventListener("click", (event) => {
    var idImage = document.getElementById('image_id').value;
    var data = {
        "id": idImage
    }
    socket.emit("delete_image_server", data)
});