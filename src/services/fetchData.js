/**
 * Realiza una petición HTTP genérica y retorna la respuesta como JSON.
 *
 * Detecta automáticamente si el body es FormData para no forzar el header
 * Content-Type (el browser lo establece con el boundary correcto).
 * Para métodos DELETE retorna null en lugar de intentar parsear JSON.
 *
 * @param {string} url - URL completa del endpoint a consumir.
 * @param {string} method - Método HTTP (GET, POST, PUT, DELETE, etc.).
 * @param {Object|FormData|null} body - Cuerpo de la petición. null para GET/DELETE.
 * @returns {Promise<Object|null>} Promesa que resuelve con el JSON de la respuesta
 *   o null en caso de DELETE exitoso.
 * @throws {Error} Si la respuesta HTTP no es ok (status >= 400).
 */
function fetchData(url, method, body = null) {
    const options = {
        method: method,
    };

    if (body instanceof FormData) {
        options.body = body;
        // Do not set Content-Type header when using FormData
    } else {
        options.headers = {
            "Content-Type": "application/json",
        };
        if (body && method !== "GET" && method !== "HEAD") {
            options.body = JSON.stringify(body);
        }
    }

    return fetch(url, options)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }
            return method === "DELETE" ? null : response.json();
        })
        .catch((error) => {
            console.error("Error al conectar", error.message);
            throw error;
        });
}

export default fetchData;
