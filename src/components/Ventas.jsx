import { useState, useEffect } from "react";

export function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [totalVenta, setTotalVenta] = useState(0);
  const [shouldRefresh, setShouldRefresh] = useState(false); // Estado para controlar la actualización

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

  function handleSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    // Convertir FormData a un objeto JSON
    const data = {
      nombre: formData.get("articulo"),
      valor: parseFloat(formData.get("valor")),
    };

    postVentas(form.method, data);
  }

  // get de diarios vendidos
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

  function handleDelete (){
    console.log('borrar')
  }

  return (
    <>
      <section className="contenedor-ingreso-ventas">
        <form method="post" onSubmit={handleSubmit}>
          <input
            type="text"
            name="articulo"
            placeholder="Ingrese el nombre de la venta"
          />
          <input type="number" name="valor" placeholder="Valor" />
          <button type="submit">Cargar venta</button>
        </form>
      </section>

      <section className="contenedor-ventas">
        {ventas.map((diario) => (
          <div
            key={diario.id}
            className="contenedor-diarios"
            style={{
              backgroundColor: diario.index % 2 === 0 ? "lightgrey" : "white",
            }}
          >
            <h3>{diario.nombre}</h3>
            <p>$ {diario.valor}</p>
          </div>
        ))}

        <div className="contenedor-total">
          <p>
            <strong>Total del día: </strong> ${" "}
            {totalVenta ? totalVenta : "Todavía no hay ventas"}
          </p>
        </div>

        <div className="contenedor-button">
          <button onClick={handleDelete}>
            Limpiar venta
          </button>
        </div>
      </section>
    </>
  );
}
