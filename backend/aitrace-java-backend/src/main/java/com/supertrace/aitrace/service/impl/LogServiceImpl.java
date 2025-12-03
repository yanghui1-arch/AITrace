package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.Project;
import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.repository.ProjectRepository;
import com.supertrace.aitrace.service.LogService;
import com.supertrace.aitrace.service.ProjectService;
import com.supertrace.aitrace.service.StepService;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class LogServiceImpl implements LogService {
    private final ProjectRepository projectRepository;
    private final ProjectService projectService;
    private final StepService stepService;

    /**
     * Log step
     * Log a step with a project. If user doesn't create a project given projectName the function will create a whole new for user.
     *
     * @param userId user uuid
     * @param logStepRequest log step request
     * @return step user uuid
     */
    @Override
    public UUID logStep(@NotNull UUID userId, @NotNull LogStepRequest logStepRequest) {
        String projectName = logStepRequest.getProjectName();
        List<Project> projects = this.projectRepository.findProjectsByName(projectName);
        Project projectOwnedByUserId = projects.stream()
            .filter(project -> project.getUserId().equals(userId))
            .findFirst()
            // Later in the procedure log something to remind user hasn't this project
            .orElseGet( () -> projectService.createNewProjectByProgram(projectName, userId));
        return stepService.logStep(userId, logStepRequest, projectOwnedByUserId.getId());
    }
}
