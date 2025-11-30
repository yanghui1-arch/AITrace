import http from "./http"


type RequestDataType = {
    projectName: string
    projectDescription: string
}

type ReturnCreateProjectNameType = string
type Project = {
    projectName: string
    description: string
    averageDuration: number
    cost: number
    createdTimestamp: string
    lastUpdateTimestamp: string
}

type Response<T> = {
    code: number,
    message: string,
    data: T
}

export const projectApi = {
    createNewProject({
        projectName,
        projectDescription,
    }: RequestDataType) {
        return http.post<Response<ReturnCreateProjectNameType>>(
            "/v0/project/create_new_project",
            {projectName, projectDescription},
        )
    },

    getAllProjects() {
        return http.get<Response<Project[]>> (
            "/v0/project/get_all_projects"
        )
    }
};