import http from "./http";

type DataType = {
  token: string,
  userName: string,
  avatar: string,
}

type Response<T> = {
  code: number,
  message: string,
  data: T
}

/* Authentication api */
export const authApi = {
  authenticate(code: string) {
    return http.get<Response<DataType>>(
      `/auth/github/callback?code=${code}`
    );
  },

  me() {
    return http.get<Response<DataType>>(
      "/auth/me"
    )
  }
};
