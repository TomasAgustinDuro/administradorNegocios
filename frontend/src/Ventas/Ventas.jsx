/**
 * Página de Ventas.
 *
 * Lista todas las ventas registradas mostrando total, status y fecha.
 * Permite cancelar ventas activas mediante un botón por cada registro.
 */

import { useState, useEffect } from "react";
import fetchData from "../services/fetchData";
import styles from "./ventas.module.css";
import VentasForm from "./components/VentasForm";

const API_URL = import.meta.env.VITE_API_URL;

/**
 * Formatea un string ISO de fecha a formato legible (ej: "15 jun 2025, 14:30").
 *
 * @param {string} isoDate - Fecha en formato ISO del backend.
 * @returns {string} Fecha formateada en español.
 */
function formatDate(isoDate) {
  const date = new Date(isoDate);

  return date.toLocaleDateString("es-AR", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [productos, setProductos] = useState([]);
  const [refreshKey, setRefreshKey] = useState(0);

  /**
   * Cancela una venta activa y actualiza su status en la lista local.
   *
   * @param {number} ventaId - ID de la venta a cancelar.
   */
  function handleCancel(ventaId) {
    fetchData(`${API_URL}/sales/${ventaId}/cancel`, "POST")
      .then((cancelledSale) => {
        setVentas(ventas.map((v) => (v.id === ventaId ? cancelledSale : v)));
      })
      .catch((error) => {
        console.error("Error al cancelar venta:", error.message);
      });
  }

  /** Dispara un re-fetch de la lista de ventas. */
  function refreshSales() {
    setRefreshKey((prev) => prev + 1);
  }

  useEffect(() => {
    fetchData(`${API_URL}/sales/`, "GET")
      .then((data) => {
        setVentas(data);
      })
      .catch((error) => {
        console.error("Error al obtener ventas:", error.message);
      });

    fetchData(`${API_URL}/products/`, "GET")
      .then((data) => {
        setProductos(data);
      })
      .catch((error) => {
        console.error("Error al obtener productos:", error.message);
      });
  }, [refreshKey]);

  /**
   * Genera un resumen legible de los ítems de una venta.
   * Cruza product_id con la lista de productos para mostrar nombres.
   *
   * @param {Array} items - Lista de ítems de la venta.
   * @returns {string} Descripción tipo "Coca x2, Pan x1".
   */
  function buildSaleSummary(items) {
    return items
      .map((item) => {
        const product = productos.find((p) => p.id === item.product_id);
        const productName = product ? product.name : `#${item.product_id}`;
        return `${productName} ×${item.quantity}`;
      })
      .join(", ");
  }

  return (
    <section className={styles.salesSection}>
      <VentasForm onSaleCreated={refreshSales} />

      <div className={styles.listContainer}>
        {ventas.map((venta) => (
          <div key={venta.id} className={styles.salesItem}>
            <div>
              <h3>${venta.total}</h3>
              <p className={styles.saleSummary}>
                {buildSaleSummary(venta.items)}
              </p>
            </div>
            <p>{venta.status}</p>
            <p>{formatDate(venta.date)}</p>
            <button onClick={() => handleCancel(venta.id)}>Cancelar</button>
          </div>
        ))}
      </div>
    </section>
  );
}
