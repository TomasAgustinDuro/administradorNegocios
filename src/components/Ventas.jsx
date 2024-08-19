import { useState, useEffect, useRef } from "react";

export function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [totalVenta, setTotalVenta] = useState(0);
  const [shouldRefresh, setShouldRefresh] = useState(false);
  const articuloRef = useRef(null);
  const valorRef = useRef(null);

  async function postVentas(formMethod, formData) {
    const url = "http://localhost:8000/diarios/api/diarios/"; // Asegúrate de que la URL sea correcta
    try {
      const response = await fetch(url, {
        method: formMethod,
        headers: {
          "Content-Type": "application/json", // Tipo de contenido correcto
        },
        body: JSON.stringify(formData), // Convertir formData a JSON
      });

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      setShouldRefresh((prev) => !prev);
    } catch (error) {
      console.error(error.message);
    }
  }

  function handleDelete(diarioId) {
    const url = `http://localhost:8000/diarios/api/diarios/${diarioId}/`;

    fetch(url, {
      method: "DELETE",
    })
      .then((response) => {
        if (response.ok) {
          console.log(diarioId);
          console.log("diario eliminado con exito");
        } else {
          console.error("Error al eliminar diario");
        }
      })
      .catch((error) => {
        console.error("Error en la solicitud:", error);
      });
  }

  function handleDeleteAll() {
    const url = "http://localhost:8000/diarios/api/diarios/eliminar_todos/";

    fetch(url, {
      method: "DELETE",
    })
      .then((response) => {
        if (response.ok) {
          console.log("Articulos eliminado con exito");
          setVentas([]); 
          setTotalVenta(0); 
        } else {
          console.error("Error al eliminar los articulos");
        }
      })
      .catch((error) => {
        console.error("Error en la solicitud:", error);
      });
  }

  function handleSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const data = {
      nombre: formData.get("articulo"),
      valor: parseFloat(formData.get("valor")),
    };

    postVentas(form.method, data);

    articuloRef.current.value = "";
    valorRef.current.value = "";
  }

  // GET de diarios vendidos
  useEffect(() => {
    const url = "http://localhost:8000/diarios/api/diarios/";
    fetch(url, {
      method: "GET",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
        return response.json();
      })
      .then((dataVentas) => {
        const nuevasVentas = dataVentas.map((diario) => ({
          id: diario.id,
          nombre: diario.nombre,
          valor: diario.valor,
        }));

        setVentas(nuevasVentas);
        let total = 0;
        nuevasVentas.forEach((venta) => {
          total += venta.valor;
        });
        setTotalVenta(total);
      })
      .catch((error) => {
        console.error("Error al obtener datos de ventas:", error.message);
      });
  }, [shouldRefresh]);

  return (
    <>
      <section className="contenedor-ingreso-ventas">
        <form method="post" onSubmit={handleSubmit}>
          <input
            ref={articuloRef}
            type="text"
            name="articulo"
            placeholder="Ingrese el nombre de la venta"
          />
          <input
            type="number"
            ref={valorRef}
            name="valor"
            placeholder="Valor"
          />
          <button type="submit">Cargar venta</button>
        </form>
      </section>

      <section className="contenedor-ventas">
        {ventas.map((diario) => (
          <div
            key={diario.id}
            className="contenedor-diarios"
            style={{
              backgroundColor: diario.id % 2 === 0 ? "lightgrey" : "white",
            }}
          >
            <h3>{diario.nombre}</h3>
            <p>$ {diario.valor}</p>

            <button
              className="buttonDelete"
              onClick={() => {
                handleDelete(diario.id);
              }}
            >
              X
            </button>
          </div>
        ))}

        <div className="contenedor-total">
          <p>
            <strong>Total del día: </strong>
            {totalVenta ? `$ ${totalVenta}` : "Todavía no hay ventas"}
          </p>
        </div>

        <div className="contenedor-button">
          <button
            onClick={() => {
              handleDeleteAll();
            }}
          >
            Limpiar venta
          </button>
        </div>
      </section>
    </>
  );
}
