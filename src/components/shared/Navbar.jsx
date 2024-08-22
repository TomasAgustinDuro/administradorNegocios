import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <>
      <header>
        <img src="#" alt="Logo del negocio" />
        <nav>
          <ul>
            <li>
              <Link to="Ventas">Ventas</Link>
            </li>
            <li><Link to="Inventario">Inventario</Link></li>
            <li><Link to="Devoluciones">Devoluciones</Link></li>
          </ul>
        </nav>
      </header>
    </>
  );
}
