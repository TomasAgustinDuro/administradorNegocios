import { useRef, useContext,useState } from "react";
import fetchData from "../../services/fetchData";
import { ShouldRefreshContext } from "../../Context/ShouldRefreshContext";
import { Validator } from "../../Utilities/validator";
import Modal from "../../modal";

function FormularioInventario() {
  const {setShouldRefresh } = useContext(ShouldRefreshContext);
  const [errors, setErrors] = useState({}); // Estado para manejar errores

  const nombreRef = useRef(null);
  const stockRef = useRef(null);
  const vendidoRef = useRef(null);
  const codigoBarrasRef = useRef(null);

  function handlePostSubmit(e) {
    e.preventDefault();

    const formData = {
      codigo_barras: codigoBarrasRef.current.value,
      nombre: nombreRef.current.value,
      stock: parseFloat(stockRef.current.value),
      vendido: parseFloat(vendidoRef.current.value),
    };

    const validationErrors = Validator(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors); // Actualizar estado de errores
      return;
    }

    const url = "http://localhost:8000/diarios/api/inventarios/";
    fetchData(url, "POST", formData)
      .then(() => {
        setShouldRefresh((prev) => !prev);
        setErrors({}); 
        nombreRef.current.value = "";
        stockRef.current.value = "";
        codigoBarrasRef.current.value = "";
        vendidoRef.current.value = "";
      })
      .catch((error) => {
        console.error("Error al agregar artículo:", error.message);
      });
  }

  return (
    <>
      <form method="POST" onSubmit={handlePostSubmit}>
        <input
          type="text"
          ref={codigoBarrasRef}
          name="codigo"
          placeholder="Codigo"
        />
        <input type="text" ref={nombreRef} name="nombre" placeholder="Nombre" />
        <input type="number" ref={stockRef} name="stock" placeholder="Stock" />
        <input
          type="number"
          ref={vendidoRef}
          name="vendido"
          placeholder="Vendido"
        />

        <button className="button">Cargar articulo</button>
      </form>

      <Modal data={errors} />
    </>
  );
}

export default FormularioInventario;
