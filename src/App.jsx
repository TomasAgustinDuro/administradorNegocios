import "./App.css";
import MainLayout from "./MainLayout";
import { ShouldRefreshProvider } from "./Context/ShouldRefreshContext";

function App() {
  return (
    <ShouldRefreshProvider>
      <MainLayout />
    </ShouldRefreshProvider>
  );
}

export default App;
