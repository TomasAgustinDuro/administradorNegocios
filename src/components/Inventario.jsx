import articulos from '../data/inventario.json'

export function Inventario () {
     
    const mostrarInformacion = () => {
        return articulos.map((articulo, index) => (
            <div key={index}>
                <h2>Título: {articulo.titulo}</h2>
                <p>ISBN: {articulo.isbn}</p>
                <p>Cantidad: {articulo.cantidad}</p>
                <p>Devuelto: {articulo.devuelto}</p>
                <p>Pendiente: {articulo.pendiente}</p>
                <hr />
            </div>
        ));    }

    return(
        <>
        <section className='contenedor-articulo'>
                <div className='div-articulo'>
                    {mostrarInformacion()}
                </div>
            </section>
        </>
    )
}