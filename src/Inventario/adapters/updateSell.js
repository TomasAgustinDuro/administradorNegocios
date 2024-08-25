// import React from 'react'
import fetchData from "../../services/fetchData";

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
