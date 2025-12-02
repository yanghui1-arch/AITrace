package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.Project;
import com.supertrace.aitrace.domain.core.step.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.factory.StepFactory;
import com.supertrace.aitrace.repository.ProjectRepository;
import com.supertrace.aitrace.repository.StepRepository;
import com.supertrace.aitrace.service.ProjectService;
import com.supertrace.aitrace.service.StepService;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Service
@RequiredArgsConstructor
public class StepServiceImpl implements StepService {

    private final StepRepository stepRepository;
    private final ProjectRepository projectRepository;
    private final ProjectService projectService;
    private final StepFactory stepFactory;

    /**
     * Validate request and persist step.
     *
     * @param logStepRequest log step request
     * @return step id
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public UUID logStep(@NotNull UUID userId, @NotNull LogStepRequest logStepRequest) {

        Step newStep;
        // 1. merge or create step
        UUID stepId = UUID.fromString(logStepRequest.getStepId());
        Optional<Step> dbStep = stepRepository.findById(stepId);
        if (dbStep.isPresent()) {
            // enrich tags, output, model and usage
            Step step = dbStep.get();
            newStep = step.enrich(
                logStepRequest.getTags(),
                logStepRequest.getInput(),
                logStepRequest.getOutput(),
                logStepRequest.getModel(),
                logStepRequest.getUsage()
            );
        }
        else {
            // Create a new step belongs to project. Create a new project without project in database.
            String projectName = logStepRequest.getProjectName();
            List<Project> projects = this.projectRepository.findProjectsByName(projectName);
            Project projectOwnedByUserId = projects.stream()
                .filter(project -> project.getUserId().equals(userId))
                .findFirst()
                // Later in the procedure log something to remind user hasn't this project
                .orElseGet( () -> projectService.createNewProjectByProgram(projectName, userId));
            newStep = stepFactory.createStep(logStepRequest, projectOwnedByUserId.getId());
        }

        // 2. save step
        stepRepository.saveAndFlush(newStep);

        // 3. logger

        // 4. return step id
        return newStep.getId();
    }

    @Override
    public List<Step> findStepsByUserIdAndProject(UUID userId,
                                  String projectName) {
        Project project = this.projectService.getProjectByUserIdAndName(userId, projectName)
            .orElseThrow(() -> new RuntimeException("Project not found: " + projectName));
        Long projectId = project.getId();
        return this.stepRepository.findStepsByProjectId(projectId);
    }
}
