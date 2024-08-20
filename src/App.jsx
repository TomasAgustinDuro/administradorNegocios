import "./App.css";
import { Inventario } from "./components/Inventario";
import { Navbar } from "./components/shared/Navbar";
// import { Ventas } from "./components/Ventas";
// import {Devoluciones} from "./components/Devoluciones"


function App() {
  return (
    <>
      <Navbar/>
      <Inventario/>
    </>
  );
}

export default App;
