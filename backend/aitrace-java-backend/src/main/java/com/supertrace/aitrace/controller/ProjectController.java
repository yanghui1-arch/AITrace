package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.domain.Project;
import com.supertrace.aitrace.dto.project.CreateProjectRequest;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.ProjectService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

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
}
