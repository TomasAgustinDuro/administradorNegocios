import { useFormVentas } from "../hooks/useFormVentas";
import Modal from "../../Modal";

function FormVentas() {
  const { handleSubmit, articuloRef, valorRef, errors } = useFormVentas();

  return (
    <>
      <form method="post" onSubmit={handleSubmit}>
        <input
          ref={articuloRef}
          type="text"
          id="articulo"
          name="articulo"
          placeholder="Enter sale name"
        />

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

      <Modal data={errors} />
    </>
  );
}

export default FormVentas;
