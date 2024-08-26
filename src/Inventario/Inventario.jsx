import React, { useState, useEffect, useRef, useContext } from "react";
import fetchData from "../services/fetchData";
import FormularioInventario from "./components/FormularioInventario";
import { updateSell } from "./adapters/updateSell";
import { ShouldRefreshContext } from "../Context/ShouldRefreshContext";

import styles from "./inventario.module.css";

export function Inventario() {
  const [articulos, setArticulos] = useState([]);
  const { shouldRefresh, setShouldRefresh } = useContext(ShouldRefreshContext);

  const sellUpdateRefs = useRef({});

  function handleDelete(articuloCodigo) {
    const url = `http://localhost:8000/diarios/api/inventarios/${articuloCodigo}/`;
    fetchData(url, "DELETE")
      .then(() => {
        setArticulos(articulos.filter((item) => item.id !== articuloCodigo));
      })
      .catch((error) => {
        console.error("Error al eliminar artículo:", error.message);
      });
  }

  useEffect(() => {
    const url = "http://localhost:8000/diarios/api/inventarios";

    fetchData(url, "GET")
      .then((articulosInventario) => {
        const datosArticulos = articulosInventario.map((articulo) => ({
          id: articulo.id,
          nombre: articulo.nombre,
          stock: articulo.stock,
          restante: articulo.restante,
          codigoBarras: articulo.codigo_barras,
        }));

        setArticulos(datosArticulos);

        const refs = {};
        datosArticulos.forEach((articulo) => {
          refs[articulo.id] = React.createRef();
        });
        sellUpdateRefs.current = refs;
      })
      .catch((error) => {
        console.error(error.message);
      });
  }, [shouldRefresh]);

  return (
    <>
      <section className={styles.formInventory}>
        <FormularioInventario />
      </section>
      <section>
        <div className={styles.divArticulo}>
          {articulos.map((articulo, id) => (
            <div key={id}>
              <h2>{articulo.nombre}</h2>
              <p>
                <strong>Codigo:</strong> {articulo.codigoBarras}
              </p>
              <p>
                <strong>Entraron:</strong> {articulo.stock}
              </p>
              <p>
                <strong>Quedan:</strong> {articulo.restante}
              </p>

              <div className={styles.containersModifiers}>
                <button
                  className="button"
                  onClick={() => {
                    handleDelete(articulo.id);
                  }}
                >
                  Borrar elemento
                </button>

                <input
                  type="number"
                  ref={sellUpdateRefs.current[articulo.id]}
                  name="sellUpdateInput"
                  placeholder="Nuevo valor"
                />

                <button
                  className="button"
                  onClick={() => {
                    const valor =
                      sellUpdateRefs.current[articulo.id].current.value;
                    updateSell(valor, articulo.id);
                    sellUpdateRefs.current[articulo.id].current.value = "";
                    setShouldRefresh((prev) => !prev); // Alternar el estado
                  }}
                >
                  Modificar cantidad
                </button>
              </div>
              <hr />
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
