import { useRef, useContext } from "react";
import fetchData from "../../services/fetchData";
import { ShouldRefreshContext } from "../../Context/ShouldRefreshContext";
import { Validator } from "../../Utilities/validator";

function FormularioInventario() {
  const {setShouldRefresh } = useContext(ShouldRefreshContext);

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

    const errors = Validator(formData);

    if (errors.nombre || errors.stock || errors.vendido || errors.codigo_barras) {
      alert(Object.values(errors).filter(error => error).join("\n"));
      return;
    }

    const url = "http://localhost:8000/diarios/api/inventarios/";
    fetchData(url, "POST", formData)
      .then(() => {
        setShouldRefresh((prev) => !prev);
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
    </>
  );
}

export default FormularioInventario;
