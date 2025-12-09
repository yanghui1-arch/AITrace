import http from "./http"

type Response<T> = {
    code: number,
    message: string,
    data: T
}

type DeleteTracesParams = {
    deleteIds: string[]
}

export const traceApi = {

    deleteTraces({ deleteIds }: DeleteTracesParams) {
        return http.post<Response<string[]>>(
            "/v0/trace/delete",
            deleteIds,
        )
    },
}