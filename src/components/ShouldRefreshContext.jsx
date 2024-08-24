import { useState, createContext } from 'react';

const ShouldRefreshContext = createContext();

function ShouldRefreshProvider({ children }) {
    const [shouldRefresh, setShouldRefresh] = useState(false);

    return (
        <ShouldRefreshContext.Provider value={{ shouldRefresh, setShouldRefresh }}>
            {children}
        </ShouldRefreshContext.Provider>
    );
}

export { ShouldRefreshProvider, ShouldRefreshContext };
