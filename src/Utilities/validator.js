export function Validator(data) {
    const containsNumber = /\d/;
    const errors = {};
    const hoy = new Date();
  
    if (data.nombre !== undefined) {
      if (!data.nombre.trim()) {
        errors.nombre = "El nombre del artículo es necesario";
      } else if (containsNumber.test(data.nombre)) {
        errors.nombre = "El nombre no puede contener números";
      }
    }
  
    if (data.codigo_barras !== undefined) {
      const containsLetters = /[a-zA-Z]/;
  
      if (containsLetters.test(data.codigo_barras)) {
        errors.codigo_barras = "El código de barras no puede contener letras";
      } else if (isNaN(data.codigo_barras) || data.codigo_barras < 0) {
        errors.codigo_barras = "El código de barras que ingresaste no es válido";
      }
    }
  
    if (data.valor !== undefined) {
      if (typeof data.valor !== "number" || data.valor < 0) {
        errors.valor = "El valor debe ser un número positivo";
      }
    }
  
    if (data.stock !== undefined) {
      if (typeof data.stock !== "number" || data.stock < 0) {
        errors.stock = "El stock debe ser un número positivo";
      }
    }
  
    if (data.vendido !== undefined) {
      if (typeof data.vendido !== "number" || data.vendido < 0) {
        errors.vendido = "El valor vendido debe ser un número positivo";
      }
    }
  
    if (data.fecha !== undefined) {
      const dateToValidate = new Date(data.fecha);
  
      if (isNaN(dateToValidate.getTime())) {
        errors.fecha = "La fecha ingresada no es válida";
      } else if (dateToValidate <= hoy) {
        errors.fecha = "Debe escoger una fecha posterior al día de hoy";
      }

      
    }
  
    if (data.imagen !== undefined) {
      if (!data.imagen || !(data.imagen instanceof File)) {
        errors.imagen = "Debes seleccionar un archivo";
      } else {
        const tipoArchivo = data.imagen.type;
        const tiposImagen = ['image/jpeg', 'image/png', 'image/webp'];
        
        if (!tiposImagen.includes(tipoArchivo)) {
          errors.imagen = "El archivo debe ser una imagen (JPEG, PNG o GIF).";
        }
      }
    }
  
    return errors;
  }
  