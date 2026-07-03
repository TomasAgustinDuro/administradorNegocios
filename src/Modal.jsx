/**
 * Componente que muestra los mensajes de error de validación de un formulario.
 *
 * Solo se renderiza si el objeto `data` contiene al menos un error.
 * Filtra valores falsy para evitar mostrar mensajes vacíos.
 *
 * @param {{ data: Object.<string, string> }} props
 *   - `data`: Objeto donde cada clave es un campo del formulario y
 *     el valor es el mensaje de error correspondiente.
 * @returns {JSX.Element|null}
 */
function Modal({ data }) {
  const errors = data;

  return (
    <>
      {Object.keys(errors).length > 0 && (
        <div className="error-messages">
          {Object.values(errors)
            .filter((error) => error)
            .map((error, index) => (
              <div key={index}>{error}</div>
            ))}
        </div>
      )}
    </>
  );
}

export default Modal;
