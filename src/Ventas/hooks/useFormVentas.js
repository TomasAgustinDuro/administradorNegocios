import { useRef, useContext,useState } from "react";
import { ShouldRefreshContext } from "../../Context/ShouldRefreshContext";
import { Validator } from "../../Utilities/validator";

/**
 * Hook que encapsula el estado y la lógica del formulario de registro de ventas.
 *
 * Maneja la validación del formulario, el envío al backend y la limpieza
 * de los campos tras un submit exitoso. Notifica al contexto global para
 * que la lista de ventas se refresque.
 *
 * @returns {{
 *   handleSubmit: Function,
 *   articuloRef: React.RefObject,
 *   valorRef: React.RefObject,
 *   errors: Object
 * }} Handlers, refs de los inputs y errores de validación actuales.
 */
export function useFormVentas() {
  const {setShouldRefresh } = useContext(ShouldRefreshContext);
  const [errors, setErrors] = useState({})
  const articuloRef = useRef(null);
  const valorRef = useRef(null);

  /**
   * Valida y envía el formulario de venta al backend.
   *
   * Extrae los valores de los inputs via FormData, los valida con `Validator`
   * y, si son válidos, los envía al endpoint de diarios. Limpia los campos
   * y dispara el refresco global al terminar.
   *
   * @param {React.FormEvent<HTMLFormElement>} e - Evento submit del formulario.
   */
  function handleSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const data = {
      nombre: formData.get("articulo"),
      valor: parseFloat(formData.get("valor")),
    };
  
    const validationErrors = Validator(data);
  
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors); 
      return;
    }

    postVentas(form.method, data);
    setShouldRefresh((prev) => !prev)
    setErrors({}); 
    articuloRef.current.value = "";
    valorRef.current.value = "";
  }

  /**
   * Envía los datos de una nueva venta al backend via POST.
   *
   * @param {string} formMethod - Método HTTP del formulario (siempre "post").
   * @param {{nombre: string, valor: number}} formData - Datos validados de la venta.
   * @returns {Promise<void>}
   */
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
    errors,
  };
}
