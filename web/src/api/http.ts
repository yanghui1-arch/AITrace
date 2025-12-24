import { MWIN_JWT } from "@/types/storage-const";
import axios from "axios";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem(MWIN_JWT);
  if (token) {
    config.headers["AT-token"] = token;
  }
  return config;
});

/* TODO: Keep it now. Later improve it. */
http.interceptors.response.use(
  (res) => res,
  (error) => {
    const status = error.response?.status;
    const message =
      error.response?.data?.message || error.message || "Request Error";

    /* 401 means not authenticated */
    if (status == 401) {
      /* Clear stale token and avoid redirect loop when already on /login */
      localStorage.removeItem(MWIN_JWT);
      const currentPath = window.location.pathname;
      if (currentPath !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(new Error(message));
  }
);

export default http;
