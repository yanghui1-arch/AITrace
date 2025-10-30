import "./App.css";
import { ThemeProvider } from "./components/ui/theme-provider";
import Dashboard from "./pages/dashboard";

function App() {
  return (
    <>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <Dashboard />
      </ThemeProvider>
    </>
  );
}

export default App;
