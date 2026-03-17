var socket = io();

document.getElementById('public_toggle').addEventListener("change", (event)=> {
    var serverId = document.getElementById("server_id").value;
    var data = {}
    if (event.target.checked) {
        data = {
            "id": serverId,
            "public": true
        }
    } else {
        data = {
            "id": serverId,
            "public": false
        }
    }
    socket.emit("change_visibility", data);
});