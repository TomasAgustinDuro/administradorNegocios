// import React from 'react'
import fetchData from "../../services/fetchData";

/**
 * Envía una solicitud PUT para actualizar la cantidad vendida de un artículo.
 *
 * El campo `vendido` en el backend es incremental: el valor enviado se suma
 * al vendido acumulado existente, no lo reemplaza.
 *
 * @param {string|number} valor - Cantidad vendida a agregar al acumulado actual.
 * @param {number} articuloCodigo - ID del artículo de inventario a actualizar.
 * @returns {void}
 */
export function updateSell(valor, articuloCodigo) {
  const url = `http://localhost:8000/diarios/api/inventarios/${articuloCodigo}/`;

  const dataUpdate = {
    vendido: valor,
  };

  fetchData(url, "PUT", dataUpdate)
    .then(() => {})
    .catch((error) => {
      console.error("Error en la solicitud:", error.message);
    });

  
}
