import fetchData from "../services/fetchData";

export function DeleteTicket(ticketId, devoluciones) {
  const url = `http://localhost:8000/diarios/api/devoluciones/${ticketId}/`;

  fetchData(url, "DELETE")
    .then(() => {
     return devoluciones.filter((item) => item.id !== ticketId);
    })
    .catch((error) => {
      console.error(error.message);
    });
}
