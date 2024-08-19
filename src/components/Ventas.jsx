import vendido from "../data/vendido.json";
import { useState, useEffect } from "react";

export function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [totalVenta, setTotalVenta] = useState(0)

  useEffect(() => {
    const nuevasVentas = vendido.map((diario) => ({
      index:diario.index,
      nombre: diario.nombre,
      valor: diario.valor,
    }));
      setVentas(nuevasVentas);

      let total = 0
      
      nuevasVentas.map((venta) => {
        total += venta.valor
        
      })
      
      console.log(total)
      setTotalVenta(total)
  }, []); 


  
  return (
    <>
      <section className="contenedor-ingreso-ventas">
        <form action="">
          <input
            type="text"
            name="articulo"
            id=""
            placeholder="ingrese el nombre de la venta"
          />
          <input type="number" name="" id="" placeholder="valor" />
          <button>Cargar venta</button>
        </form>
      </section>

      <section className="contenedor-ventas">
        {ventas.map((diario) => (
          <div key={diario.index} className="contenedor-diarios" style={{
            backgroundColor: diario.index % 2 === 0 ? 'lightgrey' : 'white'
        }}>
            <h3>{diario.nombre}</h3>
            <p>$ {diario.valor}</p>
          </div>
        ))}

        <div className="contenedor-total">
        <p><strong>Total dia: </strong> $ {totalVenta ? totalVenta : 'Todavia no hay ventas'}</p>
        </div>
      </section>
    </>
  );
}
