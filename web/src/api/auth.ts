import http from "./http";

type DataType = {
  token: string
  userId: string
}

type Response = {
  code: number,
  message: string,
  data: DataType
}

/* Authentication api */
export const authApi = {
  authenticate(code: string) {
    return http.get<Response>(
      `/auth/github/callback?code=${code}`
    );
  },
};
