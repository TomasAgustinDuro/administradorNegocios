/**
 * Formulario de registro de ventas.
 *
 * Permite seleccionar productos del catálogo, definir cantidades,
 * armar un carrito de ítems y confirmar la venta enviándola al backend.
 */

import PropTypes from "prop-types";
import { useState, useEffect } from "react";
import fetchData from "../../services/fetchData";
import styles from "../ventas.module.css";

const API_URL = import.meta.env.VITE_API_URL;

function VentasForm({ onSaleCreated }) {
  const [productos, setProductos] = useState([]);
  const [carrito, setCarrito] = useState([]);

  useEffect(() => {
    fetchData(`${API_URL}/products/`, "GET")
      .then((data) => setProductos(data))
      .catch((error) => console.error(error.message));
  }, []);

  /**
   * Lee el producto seleccionado y la cantidad del form,
   * y los agrega al carrito local.
   *
   * @param {Event} e - Evento del click en el botón "Agregar".
   */
  function handleAddItem(e) {
    e.preventDefault();

    const formData = new FormData(e.target.closest("form"));
    const productId = parseInt(formData.get("productId"));
    const quantity = parseInt(formData.get("quantity"));

    setCarrito([...carrito, { product_id: productId, quantity: quantity }]);
  }

  /**
   * Envía el carrito completo al backend como una nueva venta
   * y limpia el carrito al confirmar exitosamente.
   */
  function handleConfirmSale() {
    fetchData(`${API_URL}/sales/`, "POST", { items: carrito })
      .then(() => {
        setCarrito([]);
        onSaleCreated();
      })
      .catch((error) => console.error(error.message));
  }

  return (
    <div className={styles.formPanel}>
      <h3>Nueva venta</h3>

      <form>
        <select name="productId">
          <option value="">Seleccionar producto</option>
          {productos.map((producto) => (
            <option key={producto.id} value={producto.id}>
              {producto.name} - ${producto.price}
            </option>
          ))}
        </select>

        <input type="number" min="1" name="quantity" placeholder="Cantidad" />

        <button className="button" type="button" onClick={handleAddItem}>
          Agregar
        </button>
      </form>

      <ul className={styles.cartList}>
        {carrito.map((item, index) => (
          <li key={index} className={styles.cartItem}>
            <span>Producto #{item.product_id}</span>
            <span>× {item.quantity}</span>
          </li>
        ))}
      </ul>

      <button
        className="button"
        type="button"
        onClick={handleConfirmSale}
        disabled={carrito.length === 0}
      >
        Confirmar venta
      </button>
    </div>
  );
}

VentasForm.propTypes = {
  onSaleCreated: PropTypes.func.isRequired,
};

export default VentasForm;
