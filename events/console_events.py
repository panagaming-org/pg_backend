from extensions import socketio, db
from flask_socketio import emit
from models.entity.Console import Console
import multiprocessing

@socketio.on('send_rcon_command')
def handle_rcon_command(data):
    command = data["command"]
    ip = data["host"]
    port = int(data["port"])
    passwd = data["passwd"]

    print(data)
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=mcrcon.execute_mc_command, 
        args=(command, ip, port, passwd, result_queue)
    )
    
    process.start()
    process.join()

    response = result_queue.get()
    response = mcrcon.clean_output(response)

    emit('server_output', {'output': response})

