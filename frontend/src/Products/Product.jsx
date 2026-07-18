/**
 * Página de Productos.
 *
 * Lista todos los productos del catálogo en un grid de tarjetas.
 * Permite eliminar productos mediante un botón en cada tarjeta.
 */

import { useState, useEffect } from "react";
import fetchData from "../services/fetchData";
import ProductForm from "./components/ProductForm";
import styles from "./inventario.module.css";

const API_URL = import.meta.env.VITE_API_URL;

export function Product() {
  const [productos, setProductos] = useState([]);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    fetchData(`${API_URL}/products/`, "GET")
      .then((data) => {
        setProductos(data);
      })
      .catch((error) => {
        console.error(error.message);
      });
  }, [refreshKey]);

  /** Dispara un re-fetch de la lista de productos. */
  function refreshProducts() {
    setRefreshKey((prev) => prev + 1);
  }

  /**
   * Elimina un producto del catálogo y actualiza la lista local.
   *
   * @param {number} productoId - ID del producto a eliminar.
   */
  function handleDelete(productoId) {
    fetchData(`${API_URL}/products/${productoId}`, "DELETE")
      .then(() => {
        setProductos(productos.filter((item) => item.id !== productoId));
      })
      .catch((error) => {
        console.error("Error al eliminar artículo:", error.message);
      });
  }

  return (
    <section className={styles.productsSection}>
      <ProductForm onProductCreated={refreshProducts} />

      <div className={styles.productsGrid}>
        {productos.map((producto) => (
          <div key={producto.id} className={styles.productCard}>
            <h2>{producto.name}</h2>
            <p>
              <strong>Precio:</strong> ${producto.price}
            </p>
            <p>
              <strong>Stock:</strong> {producto.quantity}
            </p>
            <button
              className="button"
              onClick={() => handleDelete(producto.id)}
            >
              Eliminar
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}
