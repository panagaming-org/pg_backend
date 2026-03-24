var socket = io();

/**
 * Función que permite cambiar el estado de un servidor.
 */
const changeVisibility = async (idServer, checked) => {
    try{
        await fetch("http://127.0.0.1:5000/api/servers/update/public", {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: idServer,
                public: checked
            })
        });
    } catch (error) {
        console.error("Error de red: ", error);
    }
}

/**
 *  Permite cambiar el estado del servidor.
 */
const changeServerStatus = async (idServer, status) => {
    await fetch("http://127.0.0.1:5000/api/servers/update/status", {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: idServer,
            status: status
        })
    });
}


export {
    changeVisibility,
    changeServerStatus
}