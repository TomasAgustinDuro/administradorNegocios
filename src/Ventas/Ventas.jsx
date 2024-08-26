import { useState, useEffect, useContext } from "react";
import { ShouldRefreshContext } from "../Context/ShouldRefreshContext";
import FormVentas from "./components/FormVentas";
import fetchData from "../services/fetchData";
import ventasHelps from "./services/ventasHelps";

import styles from "./ventas.module.css";

export function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [totalVenta, setTotalVenta] = useState(0);
  const { shouldRefresh,setShouldRefresh } = useContext(ShouldRefreshContext);

  const handleDelete = async (diarioId = null) => {
    const result = await ventasHelps(diarioId);

    if (result.success) {
      setShouldRefresh((prev) => !prev);
      if (result.clearAll) {
        setVentas([]); 
        setTotalVenta(0);
      }
    }
  };
 
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
      <div className={styles.container}>
        <section className={styles.inputContainer}>
          <FormVentas />
        </section>

        <section className={styles.listContainer}>
          {ventas.map((diario) => (
            <div
              key={diario.id}
              className={styles.salesItem}
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
            <div className={styles.sumaryContainer}>
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
