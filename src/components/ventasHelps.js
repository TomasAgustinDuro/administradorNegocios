import {useContext} from "react";
import { ShouldRefreshContext } from "./ShouldRefreshContext";

function ventasHelps(diarioId = null) {
  const { shouldRefresh, setShouldRefresh } = useContext(ShouldRefreshContext);

  const url = diarioId
    ? `http://localhost:8000/diarios/api/diarios/${diarioId}/`
    : "http://localhost:8000/diarios/api/diarios/eliminar_todos/";

  fetch(url, {
    method: "DELETE",
  })
    .then((response) => {
      if (response.ok) {
        console.log(
          diarioId
            ? `Diario ${diarioId} eliminado con éxito`
            : "Todos los artículos eliminados con éxito"
        );

        if (!diarioId) {
          setVentas([]); // Reinicia el estado para eliminar todas las ventas del UI
          setTotalVenta(0);
        }

        setShouldRefresh((prev) => !prev);
      } else {
        console.error(
          `Error al eliminar ${diarioId ? "diario" : "todos los artículos"}`
        );
      }
    })
    .catch((error) => {
      console.error("Error en la solicitud:", error);
    });
}

export default ventasHelps;
