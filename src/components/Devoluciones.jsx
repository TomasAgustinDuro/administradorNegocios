// import devoluciones from "../data/devoluciones.json";
import { useEffect, useState } from "react";

export function Devoluciones() {
  const [devoluciones, setDevoluciones] = useState([]);
  const [shouldRefresh, setShouldRefresh] = useState(false);

  useEffect(() => {
    const url = "http://localhost:8000/diarios/api/devoluciones/";

    fetch(url, {
      method: "GET",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
        return response.json();
      })
      .then((devoluciones) => {
        const devolucion = devoluciones.map((item) => ({
          id: item.id,
          url: item.imagen,
          fecha: item.fecha,
        }));

        setDevoluciones(devolucion);
      })
      .catch((error) => {
        console.error(error.message);
      });
  },[shouldRefresh]);

  function uploadTicketReturns(formMethod, formData) {
    const url = "http://localhost:8000/diarios/api/devoluciones/";

    fetch(url, {
      method: formMethod,
      body: formData
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
        setShouldRefresh((prev) => !prev)
      })
      .catch((error) => {
        console.error(error.message);
      });
  }

  function deleteTicketReturns(ticketId){
    const url = `http://localhost:8000/diarios/api/devoluciones/${ticketId}/`

    fetch(url, {
      method: "DELETE",
    })
      .then((response) => {
        if (response.ok) {
          console.log("Devolucion eliminada con exito")
          setDevoluciones(devoluciones.filter((item) => item.id !== ticketId))
          
        } else {
          console.error("Error al eliminar articulo")
        }
        setShouldRefresh((prev) => !prev)
      })
      .catch((error) => {
        console.error(error.message);
      });
  }

  const mostrarBoletas = () => {
    const baseUrl = "http://localhost:8000";
  
    return devoluciones.map((devolucion) => (
      <div key={devolucion.id} className="boleta">
        <a href={`${baseUrl}${devolucion.url}`} target="_blank" rel="noopener noreferrer">
          <img src={`${baseUrl}${devolucion.url}`} alt={`Imagen ${devolucion.id}`} />
        </a>
        <p>{devolucion.fecha}</p>

        <button
          onClick={() => {
            deleteTicketReturns(devolucion.id)
          }}
        >
          Borrar
        </button>
      </div>
    ));
  };
  

  function handleSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    uploadTicketReturns(form.method, formData);

  }

  return (
    <>
      <section className="section-upload-ticket">
        👩
        <form method="POST" encType="multipart/form-data" onSubmit={handleSubmit}>
          <input
            type="file"
            accept="image/*"
            name="imagen"
            placeholder="Carga tu imagen aca"
          />
          <input type="date" name="fecha" id="" placeholder="¿Que dia es hoy?" />

          <button>
            Cargar imagen
          </button>
        </form>
      </section>

      <section className="contenedor-boletas">
        <div className="boletas">{mostrarBoletas()}</div>
      </section>
    </>
  );
}
