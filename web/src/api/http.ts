import { AT_JWT } from "@/types/storage-const";
import axios from "axios";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem(AT_JWT);
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
      window.location.href = "/login";
      return ;
    }

    return Promise.reject(new Error(message));
  }
);

export default http;
