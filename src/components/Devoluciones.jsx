// import devoluciones from "../data/devoluciones.json";
import { useEffect, useState, useContext } from "react";
import fetchData from "../services/fetchData";
import FormDevoluciones from "./FormDevoluciones";
import { ShouldRefreshContext } from "./ShouldRefreshContext";
import { DeleteTicket } from "./DeleteTicket";

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
                      DeleteTicket(devolucion.id, devoluciones)
                      setDevoluciones(devoluciones)
                      setShouldRefresh((prev) => !prev)
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
