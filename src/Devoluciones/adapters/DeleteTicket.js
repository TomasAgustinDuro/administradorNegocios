import fetchData from "../../services/fetchData";

export function DeleteTicket(ticketId) {
  const url = `http://localhost:8000/diarios/api/devoluciones/${ticketId}/`;

  return fetchData(url, "DELETE")
    .then(() => {
      // No es necesario devolver la lista filtrada aquí
    })
    .catch((error) => {
      console.error("Error al eliminar el ticket:", error.message);
      throw error; // Relanza el error para manejarlo en la función que llama
    });
}
