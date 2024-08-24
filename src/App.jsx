import "./App.css";
import MainLayout from "./components/MainLayout";
import { ShouldRefreshProvider } from "./components/ShouldRefreshContext";

function App() {
  return (
    <ShouldRefreshProvider>
      <MainLayout />
    </ShouldRefreshProvider>
  );
}

export default App;
