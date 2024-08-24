// services/fetchData.js
function fetchData(url, method, body = null) {
    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
    };

    // Añadir el cuerpo solo si no es un método que no debe tener cuerpo como GET o HEAD
    if (body && method !== "GET" && method !== "HEAD") {
        options.body = JSON.stringify(body);
    } else if (method === "GET" || method === "HEAD") {
        // Asegúrate de que no se envíe el cuerpo en métodos GET o HEAD
        options.body = undefined;
    }

    return fetch(url, options)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }
            // Para DELETE devolvemos null, para otros métodos devolvemos JSON si hay cuerpo
            return method === "DELETE" ? null : response.json();
        })
        .catch((error) => {
            console.error("Error al conectar", error.message);
            throw error; // Propaga el error para que el componente pueda manejarlo
        });
}

export default fetchData;
