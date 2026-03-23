var socket = io();

/**
 * Función que permite cambiar el estado de un servidor.
 */
function changeVisibility(idServer, checked) {
    var data = {
        "id": idServer,
        "public": checked
    }
    socket.emit("change_server_visibility", data);
}

/**
 *  Permite cambiar el estado del servidor.
 */
function changeServerStatus(idServer, status) {
    var data = {
        "id": idServer,
        "status": status
    }
    socket.emit("change_server_status", data);
}


export {
    changeVisibility,
    changeServerStatus
}