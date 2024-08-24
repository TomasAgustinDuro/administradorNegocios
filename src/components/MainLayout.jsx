import { Navbar } from "./shared/Navbar";
import { Devoluciones } from "./Devoluciones";
import { Inventario } from "./Inventario";
import { Ventas } from "./Ventas";
import { Route, Routes } from "react-router-dom";

function MainLayout() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Ventas />} />
        <Route path="Ventas" element={<Ventas />} />
        <Route path="Inventario" element={<Inventario />} />
        <Route path="Devoluciones" element={<Devoluciones />} />
      </Routes>
    </>
  );
}

export default MainLayout;
