import fetchData from "../../services/fetchData";

/**
 * Envía una solicitud DELETE para eliminar una devolución por su ID.
 *
 * Delega la petición HTTP a `fetchData` y relanza el error si falla,
 * para que el componente llamador pueda manejarlo con su propio estado.
 *
 * @param {number} ticketId - ID de la devolución a eliminar.
 * @returns {Promise<void>} Promesa que resuelve si la eliminación fue exitosa.
 * @throws {Error} Si la petición HTTP falla.
 */
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
