function ventasHelps(diarioId = null) {
 const url = diarioId
    ? `http://localhost:8000/diarios/api/diarios/${diarioId}/`
    : "http://localhost:8000/diarios/api/diarios/eliminar_todos/";

  return fetch(url, {
    method: "DELETE",
  })
    .then((response) => {
      if (response.ok) {
        console.log(
          diarioId
            ? `Diario ${diarioId} eliminado con éxito`
            : "Todos los artículos eliminados con éxito"
        );


        return {
          success: true,
          clearAll: !diarioId, // Indica si se eliminaron todos los artículos
        };
      } else {
        console.error(
          `Error al eliminar ${diarioId ? "diario" : "todos los artículos"}`
        );
        return { success: false };
      }
    })
    .catch((error) => {
      console.error("Error en la solicitud:", error);
      return { success: false };
    });
}

export default ventasHelps;
