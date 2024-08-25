// import devoluciones from "../data/devoluciones.json";
import { useEffect, useState, useContext } from "react";
import fetchData from "../services/fetchData";
import FormDevoluciones from "./components/FormDevoluciones";
import { ShouldRefreshContext } from "../Context/ShouldRefreshContext";
import { DeleteTicket } from "./adapters/DeleteTicket";

export function Devoluciones() {
  const [devoluciones, setDevoluciones] = useState([]);
  const { shouldRefresh, setShouldRefresh } = useContext(ShouldRefreshContext);

  const baseUrl = "http://localhost:8000";

  useEffect(() => {
    const url = "http://localhost:8000/diarios/api/devoluciones/";

    fetchData(url, "GET")
      .then((devoluciones) => {
        const devolucion = devoluciones.map((item) => ({
          id: item.id,
          url: item.imagen,
          fecha: item.fecha,
        }));

        setDevoluciones(devolucion);
      })
      .catch((error) => {
        console.error(error.message);
      });
  }, [shouldRefresh]);

  const handleDelete = (id) => {
    DeleteTicket(id)
      .then(() => {
        setDevoluciones((prevDevoluciones) =>
          prevDevoluciones.filter((devolucion) => devolucion.id !== id)
        );
        setShouldRefresh((prev) => !prev); // Alterna shouldRefresh para activar useEffect
      })
      .catch((error) => {
        console.error("Error al eliminar el ticket:", error.message);
      });
  };
  

  return (
    <>
      <section className="section-upload-ticket">
        <FormDevoluciones />
      </section>

      <section className="tickets-container">
        {devoluciones.length > 0 ? (
          <div className="tickets">
            {devoluciones.map((devolucion) => (
              <div key={devolucion.id} className="ticket">
                <a
                  href={`${baseUrl}${devolucion.url}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <img
                    src={`${baseUrl}${devolucion.url}`}
                    alt={`Imagen ${devolucion.id}`}
                  />
                </a>
                <div className="footer-ticket">
                  <p>{devolucion.fecha}</p>

                  <button
                    className="button"
                    onClick={() => {
                      handleDelete(devolucion.id);
                    }}
                  >
                    Borrar
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <h3>No hay boletas cargadas</h3>
        )}
      </section>
    </>
  );
}
