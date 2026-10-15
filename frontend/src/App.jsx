/**
 * Componente raíz de la aplicación.
 *
 * Define el layout principal (Navbar + rutas) sin providers externos.
 * Las rutas disponibles son Products (home) y Sales.
 */

import "./App.css";
import { Navbar } from "./shared/Navbar";
import { Product } from "./Products/Product";
import { Ventas } from "./Ventas/Ventas";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Product />} />
        <Route path="/sales" element={<Ventas />} />
      </Routes>
    </>
  );
}

export default App;
