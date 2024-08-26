// import devoluciones from "../data/devoluciones.json";
import { useEffect, useState, useContext } from "react";
import fetchData from "../services/fetchData";
import FormDevoluciones from "./components/FormDevoluciones";
import { ShouldRefreshContext } from "../Context/ShouldRefreshContext";
import { DeleteTicket } from "./adapters/DeleteTicket";

import styles from './devoluciones.module.css'

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
        setShouldRefresh((prev) => !prev);
      })
      .catch((error) => {
        console.error("Error al eliminar el ticket:", error.message);
      });
  };
  

  return (
    <>
      <section className={styles.uploadTicket}>
        <FormDevoluciones />
      </section>

      <section className={styles.listTickets}>
        {devoluciones.length > 0 ? (
          <div className={styles.tickets}>
            {devoluciones.map((devolucion) => (
              <div key={devolucion.id} className={styles.ticket}>
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
                <div className={styles.footerTicket}>
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
