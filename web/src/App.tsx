import "./App.css";
import { ThemeProvider } from "./components/ui/theme-provider";
import { Toaster } from "@/components/ui/sonner";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AppLayout } from "./layouts/app-layout";
import OverviewPage from "./pages/overview";
import ProjectsPage from "./pages/projects";
import ProjectDetailPage from "./pages/projects/track";
import LoginPage from "./pages/login";
import GitHubAuthPage from "./pages/auth/github";
import { APIKeyPage } from "./pages/apikey";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <Routes>
          <Route element={<AppLayout />}>
            <Route index element={<Navigate to="/overview" replace />} />
            <Route path="/overview" element={<OverviewPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/projects/:name" element={<ProjectDetailPage />} />
            <Route path="/apikey" element={<APIKeyPage />} />
          </Route>
          <Route path="/login" element={<LoginPage />}/>
          <Route path="/auth/github/callback" element={<GitHubAuthPage />} />
        </Routes>
      </ThemeProvider>
      <Toaster position="top-center" richColors />
    </BrowserRouter>
  );
}

export default App;
