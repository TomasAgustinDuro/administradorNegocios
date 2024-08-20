export function CargaInventario() {
  
  async function postArticulo(formMethod,formData) {
    const url = "http://localhost:8000/diarios/api/inventarios/";
    try {
      const response = await fetch(url, {
        method: formMethod,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData), 
      });

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    } catch (error) {
      console.error(error.message);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form)

    const data = {
      codigo_barras:formData.get("codigo"),
      nombre: formData.get("nombre"),
      stock: formData.get("stock"),
      vendido: formData.get("vendido")
    }

    postArticulo(form.method, data)

  }

  return (
    <>
      <form method="POST" onSubmit={handleSubmit}>
        <input type="text" name="codigo" placeholder="Codigo" />
        <input type="text" name="nombre" placeholder="Nombre" />
        <input type="number" name="stock" placeholder="Stock" />
        <input type="number" name="vendido" placeholder="Vendido" />

        <button>Cargar articulo</button>
      </form>
    </>
  );
}
