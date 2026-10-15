/**
 * Barra de navegación principal.
 *
 * Muestra el nombre del negocio y los links a las secciones
 * disponibles: Products (inventario) y Sales (ventas).
 */

import { Link } from "react-router-dom";
import styles from "./navbar.module.css";

export function Navbar() {
  return (
    <header className={styles.header}>
      <h1>Negocio</h1>
      <nav>
        <ul>
          <li>
            <Link to="/">Products</Link>
          </li>
          <li>
            <Link to="/sales">Sales</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}
