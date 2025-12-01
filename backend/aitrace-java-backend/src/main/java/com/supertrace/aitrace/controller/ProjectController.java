package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.domain.Project;
import com.supertrace.aitrace.dto.project.CreateProjectRequest;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.ProjectService;
import com.supertrace.aitrace.vo.project.ProjectInfoVO;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v0/project")
public class ProjectController {

    private final ProjectService projectService;

    @Autowired
    public ProjectController(ProjectService projectService) {
        this.projectService = projectService;
    }

    @PostMapping("/create_new_project")
    public ResponseEntity<APIResponse<String>> createProjectOnProjectPage(HttpServletRequest request, @RequestBody CreateProjectRequest createProjectRequest) {
        try {
            UUID userId = (UUID) request.getAttribute("userId");
            Project project = this.projectService.createNewProjectByManualCreation(createProjectRequest, userId);
            return ResponseEntity.ok(APIResponse.success(project.getName(), String.format("Create a new project successfully for user uuid: %s", userId)));
        } catch (Exception exception) {
            return ResponseEntity.badRequest().body(APIResponse.error(exception.getMessage()));
        }
    }

    @GetMapping("/get_all_projects")
    public ResponseEntity<APIResponse<List<ProjectInfoVO>>> getAllProjects(HttpServletRequest request) {
        try {
            UUID userId = (UUID) request.getAttribute("userId");
            List<Project> projects = this.projectService.getProjectsByUserId(userId);
            if (!projects.isEmpty()) {
                List<ProjectInfoVO> projectsVO = projects.stream().map(
                    p -> ProjectInfoVO.builder()
                        .projectName(p.getName())
                        .description(p.getDescription())
                        .averageDuration(p.getAverageDuration())
                        .cost(p.getCost())
                        .createdTimestamp(p.getCreatedTimestamp())
                        .lastUpdateTimestamp(p.getLastUpdateTimestamp())
                        .build()
                ).toList();
                return ResponseEntity.ok(APIResponse.success(projectsVO));
            } else {
                return ResponseEntity.ok(APIResponse.notFound("Not found projects"));
            }
        } catch (Exception exception) {
            return ResponseEntity.badRequest().body(APIResponse.error(exception.getMessage()));
        }
    }

    @PostMapping("/delete/{projectName}")
    public ResponseEntity<APIResponse<String>> deleteProject(HttpServletRequest request, @PathVariable String projectName) {
        try {
            UUID userId = (UUID) request.getAttribute("userId");
            this.projectService.deleteProject(userId, projectName);
            return ResponseEntity.ok(APIResponse.success("Project deleted successfully"));
        } catch (Exception exception) {
            return ResponseEntity.badRequest().body(APIResponse.error(exception.getMessage()));
        }
    }
}
