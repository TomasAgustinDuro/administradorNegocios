import { useState, useEffect, useContext } from "react";
import { ShouldRefreshContext } from "./ShouldRefreshContext";
import FormVentas from "../components/FormVentas";
import fetchData from "../services/fetchData";

export function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [totalVenta, setTotalVenta] = useState(0);
  const { shouldRefresh, setShouldRefresh } = useContext(ShouldRefreshContext);

  function handleDelete(diarioId = null) {
    const url = diarioId
      ? `http://localhost:8000/diarios/api/diarios/${diarioId}/`
      : "http://localhost:8000/diarios/api/diarios/eliminar_todos/";
  
    fetchData(url, "DELETE")
      .then(() => {
        console.log(
          diarioId
            ? `Diario ${diarioId} eliminado con éxito`
            : "Todos los artículos eliminados con éxito"
        );
  
        if (!diarioId) {
          setVentas([]); 
          setTotalVenta(0);
        }
  
        setShouldRefresh((prev) => !prev);
      })
      .catch((error) => {
        console.error(
          `Error al eliminar ${diarioId ? "diario" : "todos los artículos"}`,
          error.message
        );
      });
  }
 
  useEffect(() => {
    const url = "http://localhost:8000/diarios/api/diarios/";
  
    fetchData(url, "GET")
      .then((dataVentas) => {
        const nuevasVentas = dataVentas.map(({ id, nombre, valor }) => ({ id, nombre, valor }));
  
        setVentas(nuevasVentas);
        const total = nuevasVentas.reduce((sum, { valor }) => sum + valor, 0);
        setTotalVenta(total);
      })
      .catch((error) => {
        console.error('Error al obtener datos', error.message);
      });
  }, [shouldRefresh]);

  return (
    <>
      <div className="sales-management-container">
        <section className="sales-input-container">
          <FormVentas />
        </section>

        <section className="sales-list-container">
          {ventas.map((diario) => (
            <div
              key={diario.id}
              className="sales-item"
              style={{
                backgroundColor: diario.id % 2 === 0 ? "lightgrey" : "white",
              }}
            >
              <h3>{diario.nombre}</h3>
              <p>$ {diario.valor}</p>
              <button
                className="button-delete button"
                onClick={() => handleDelete(diario.id)}
              >
                X
              </button>
            </div>
          ))}

          {ventas.length > 0 ? (
            <div className="sales-summary-container">
              <p>
                <strong>Total for the day: </strong>
                {totalVenta ? `$ ${totalVenta}` : "No sales yet"}
              </p>

              <button
                className="button"
                onClick={() => {
                  handleDelete();
                }}
              >
                <span className="label">Clear all</span>
              </button>
            </div>
          ) : null}
        </section>
      </div>
    </>
  );
}
