/**
 * Valida los campos de un formulario según las reglas de negocio del sistema.
 *
 * Cada campo es validado solo si está presente en el objeto recibido,
 * permitiendo validaciones parciales (útil en formularios de edición).
 *
 * @param {Object} data - Objeto con los campos a validar. Puede incluir:
 *   @param {string}  [data.name]      - Nombre del producto (no vacío, sin números).
 *   @param {number}  [data.price]     - Precio de venta (número no negativo).
 *   @param {number}  [data.quantity]  - Cantidad en stock (número no negativo).
 * @returns {Object} Objeto con los errores encontrados. Clave = nombre del campo,
 *   valor = mensaje de error. Retorna objeto vacío si no hay errores.
 */
export function Validator(data) {
  const containsNumber = /\d/;
  const errors = {};

  if (data.name !== undefined) {
    if (!data.name.trim()) {
      errors.name = "El nombre del artículo es necesario";
    } else if (containsNumber.test(data.name)) {
      errors.name = "El nombre no puede contener números";
    }
  }

  if (data.price !== undefined) {
    if (typeof data.price !== "number" || data.price < 0) {
      errors.price = "El valor debe ser un número positivo";
    }
  }

  if (data.quantity !== undefined) {
    if (typeof data.quantity !== "number" || data.quantity < 0) {
      errors.quantity = "El stock debe ser un número positivo";
    }
  }

  return errors;
}
