var socket = io();

document.getElementById('status_select').addEventListener("change", (event) => {
    var serverId = document.getElementById("server_id").value;
    var status = event.target.value;

    var data = {
        "id": serverId,
        "status": status
    }
    socket.emit("change_server_status", data)
});