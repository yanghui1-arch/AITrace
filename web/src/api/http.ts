import axios from "axios";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

/* Temperorily don't intercept anything. In the future bearer AITrace token */
http.interceptors.request.use((config) => {

  return config;
});

/* TODO: Keep it now. Later improve it. */
http.interceptors.response.use(
  (res) => res,
  (error) => {
    const message =
      error.response?.data?.message || error.message || "Request Error";

    return Promise.reject(new Error(message));
  }
);

export default http;
