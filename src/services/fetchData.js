function fetchData(url, method) {
  return fetch(url, { method: method })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }

      return method === "DELETE" ? null : response.json();
    })
    .catch((error) => {
      console.error("Error al conectar", error.message);
      throw error; // Propaga el error para que el componente pueda manejarlo
    });
}

export default fetchData;
