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
