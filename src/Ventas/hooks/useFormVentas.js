import { useRef, useContext } from "react";
import { ShouldRefreshContext } from "../../Context/ShouldRefreshContext";

export function useFormVentas() {
  const {setShouldRefresh } = useContext(ShouldRefreshContext);
  const articuloRef = useRef(null);
  const valorRef = useRef(null);

  function handleSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const data = {
      nombre: formData.get("articulo"),
      valor: parseFloat(formData.get("valor")),
    };

    postVentas(form.method, data);
    setShouldRefresh((prev) => !prev)
    articuloRef.current.value = "";
    valorRef.current.value = "";
  }

  async function postVentas(formMethod, formData) {
    const url = "http://localhost:8000/diarios/api/diarios/"; // Asegúrate de que la URL sea correcta
    try {
      const response = await fetch(url, {
        method: formMethod,
        headers: {
          "Content-Type": "application/json", // Tipo de contenido correcto
        },
        body: JSON.stringify(formData), 
        
      });

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    } catch (error) {
      console.error(error.message);
    }
  }

  return {
    handleSubmit,
    articuloRef,
    valorRef,
  };
}
