var socket = io();

socket.on('server_output', function(data) {
    var terminal = document.getElementById('terminal');
    terminal.innerText += "> " + data.output + "\n";
    terminal.scrollTop = terminal.scrollHeight;
});

document.getElementById('command_form').addEventListener("submit", (event)=> {
    event.preventDefault();
    var host = document.getElementById("host").value;
    var passwd = document.getElementById("passwd").value;
    var port = document.getElementById("port").value;
    var command = document.getElementById('commandInput').value;

    command = {
        "command": command,
        "host": host,
        "port": port,
        "passwd": passwd
    }

    socket.emit('send_command', command);
    document.getElementById('commandInput').value = '';
});