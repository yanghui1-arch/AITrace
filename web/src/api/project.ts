import http from "./http"


type CreateNewProjectRequestDataType = {
    projectName: string
    projectDescription: string
}
type DeleteProjectRequestDataType = {
    projectName: string
}
type UpdateProjectDescriptionRequestDataType = {
    projectId: number
    newDescription: string
}

type ReturnCreateProjectNameType = string
type Project = {
    projectId: number,
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
    }: CreateNewProjectRequestDataType) {
        return http.post<Response<ReturnCreateProjectNameType>>(
            "/v0/project/create_new_project",
            {projectName, projectDescription},
        )
    },

    getAllProjects() {
        return http.get<Response<Project[]>> (
            "/v0/project/get_all_projects"
        )
    },

    updateProjects({
        projectId,
        newDescription,
    }: UpdateProjectDescriptionRequestDataType) {
        return http.post<Response<Project>> (
            `/v0/project/update/${encodeURIComponent(newDescription)}`,
            { projectId }
        )
    },

    deleteProject({
        projectName,
    }: DeleteProjectRequestDataType) {
        return http.post<Response<string>> (
            `/v0/project/delete/${projectName}`
        )
    }
};