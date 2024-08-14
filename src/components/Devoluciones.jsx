import devoluciones from "../data/devoluciones.json";

export function Devoluciones() {
  const mostrarBoletas = () => {
    return devoluciones.map((devolucion, index) => (
      <div key={index} className="boleta">
        <a href={devolucion.url_imagen} target="_blank">
          <img src={devolucion.url_imagen} alt={`Imagen ${index}`} />
        </a>
        <p>{devolucion.fecha}</p>
      </div>
    ));
  };

  return (
    <>
      <section className="contenedor-boletas">
        <div className="boletas">{mostrarBoletas()}</div>
      </section>
    </>
  );
}
