import http from "./http"

type Response<T> = {
    code: number,
    message: string,
    data: T
}

type DeleteStepsParams = {
    deleteIds: string[]
}

export const stepApi = {

    deleteSteps({ deleteIds }: DeleteStepsParams) {
        return http.post<Response<string[]>>(
            "/v0/step/delete",
            deleteIds,
        )
    },
}