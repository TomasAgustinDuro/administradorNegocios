import { Link } from "react-router-dom";
import styles from "./navbar.module.css"

export function Navbar() {
  return (
    <>
      <header className={styles.header}>
        <h1>Los mareados</h1>
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
