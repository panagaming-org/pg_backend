
/**
 * Función que permite cambiar el estado de un servidor.
 */
const changeVisibility = async (idServer, checked) => {
    try{
        await fetch("https://pg-backend-navy.vercel.app/api/servers/update/public", {
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
    try{
        await fetch("https://pg-backend-navy.vercel.app/api/servers/update/status", {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: idServer,
                status: status
            })
        });
    } catch (error) {
        console.error("Error de red: ", error)
    }
}


export {
    changeVisibility,
    changeServerStatus
}