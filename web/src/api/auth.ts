import http from "./http";

type ResponseData<T> = {
  code: number,
  message: string,
  data: T
}

/* Authentication api */
export const authApi = {
  authenticate(code: string) {
    return http.get<ResponseData<string>>(
      `/auth/github/callback?code=${code}`
    );
  },
};
