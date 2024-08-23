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
          setVentas([]); // Reinicia el estado para eliminar todas las ventas del UI
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
      <div className="sales-management-container">
        <section className="sales-input-container">
          <form method="post" onSubmit={handleSubmit}>
            <label htmlFor="articulo">Sale Name</label>
            <input
              ref={articuloRef}
              type="text"
              id="articulo"
              name="articulo"
              placeholder="Enter sale name"
            />

            <label htmlFor="valor">Value</label>
            <input
              type="number"
              ref={valorRef}
              id="valor"
              name="valor"
              placeholder="Value"
            />

            <button type="submit" className="button">
              Add Sale
            </button>
          </form>
        </section>

        <section className="sales-list-container">
          {ventas.map((diario) => (
            <div
              key={diario.id}
              className="sales-item"
              style={{
                backgroundColor: diario.id % 2 === 0 ? "lightgrey" : "white",
              }}
            >
              <h3>{diario.nombre}</h3>
              <p>$ {diario.valor}</p>
              <button
                className="button-delete button"
                onClick={() => {
                  handleDelete(diario.id);
                }}
              >
                X
              </button>
            </div>
          ))}

         {ventas.length > 0 ? ( <div className="sales-summary-container">
            <p>
              <strong>Total for the day: </strong>
              {totalVenta ? `$ ${totalVenta}` : "No sales yet"}
            </p>

            <button
              className="button"
              onClick={() => {
                handleDeleteAll();
              }}
            >
              <span className="lable">Clear all</span>
            </button>
          </div>) : null}
        </section>
      </div>
    </>
  );
}
