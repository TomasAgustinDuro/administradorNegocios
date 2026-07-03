import { useState, createContext } from 'react';

/**
 * Contexto global que indica si los componentes consumidores deben
 * refrescar sus datos desde el backend.
 *
 * Se usa como mecanismo de invalidación simple: al alternar el valor
 * booleano de `shouldRefresh`, cualquier `useEffect` que lo incluya
 * en su array de dependencias se vuelve a ejecutar.
 */
const ShouldRefreshContext = createContext();

/**
 * Proveedor del contexto ShouldRefreshContext.
 *
 * Expone `shouldRefresh` (boolean) y `setShouldRefresh` a todos los
 * componentes descendientes. Para disparar un refresco, llamar a
 * `setShouldRefresh(prev => !prev)`.
 *
 * @param {{ children: React.ReactNode }} props
 * @returns {JSX.Element}
 */
function ShouldRefreshProvider({ children }) {
    const [shouldRefresh, setShouldRefresh] = useState(false);

    return (
        <ShouldRefreshContext.Provider value={{ shouldRefresh, setShouldRefresh }}>
            {children}
        </ShouldRefreshContext.Provider>
    );
}

export { ShouldRefreshProvider, ShouldRefreshContext };
