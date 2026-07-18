/**
 * Formulario de carga de productos.
 *
 * Permite ingresar nombre, precio y stock de un nuevo producto
 * y enviarlo al backend tras validar los campos.
 */

import PropTypes from "prop-types";
import fetchData from "../../services/fetchData";
import { Validator } from "../../Utilities/validator";
import styles from "../inventario.module.css";

const API_URL = import.meta.env.VITE_API_URL;

function ProductoForm({ onProductCreated }) {
  /**
   * Valida los campos y envía el nuevo producto al backend.
   *
   * @param {Event} e - Evento submit del formulario.
   */
  function handlePostSubmit(e) {
    e.preventDefault();

    const formData = new FormData(e.target);

    const data = {
      name: formData.get("name"),
      price: parseFloat(formData.get("price")),
      quantity: parseInt(formData.get("quantity")),
    };

    const validationErrors = Validator(data);

    if (Object.keys(validationErrors).length > 0) {
      return;
    }

    fetchData(`${API_URL}/products/`, "POST", data)
      .then(() => {
        e.target.reset();
        onProductCreated();
      })
      .catch((error) => {
        console.error("Error al agregar artículo:", error.message);
      });
  }

  return (
    <div className={styles.formContainer}>
      <form method="POST" onSubmit={handlePostSubmit}>
        <input type="text" name="name" placeholder="Nombre del producto" />
        <input type="number" name="price" placeholder="Precio" />
        <input type="number" name="quantity" placeholder="Stock" />
        <button className="button">Cargar producto</button>
      </form>
    </div>
  );
}

ProductoForm.propTypes = {
  onProductCreated: PropTypes.func.isRequired,
};

export default ProductoForm;
