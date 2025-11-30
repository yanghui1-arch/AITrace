import http from "./http"


type RequestDataType = {
    projectName: string
    projectDescription: string
}

type ReturnProjectNameType = string

type Response = {
    code: number,
    message: string,
    data: ReturnProjectNameType
}

export const projectApi = {
    createNewProject({
        projectName,
        projectDescription,
    }: RequestDataType) {
        return http.post<Response>(
            "/v0/project/create_new_project",
            {projectName, projectDescription},
        )
    }
};