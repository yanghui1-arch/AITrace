package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.Project;
import com.supertrace.aitrace.dto.project.CreateProjectRequest;
import com.supertrace.aitrace.exception.project.DuplicateProjectNameException;
import com.supertrace.aitrace.repository.ProjectRepository;
import com.supertrace.aitrace.service.ProjectService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class ProjectServiceImpl implements ProjectService {

    private final ProjectRepository projectRepository;

    @Autowired
    public ProjectServiceImpl(ProjectRepository projectRepository) {
        this.projectRepository = projectRepository;
    }

    /**
     * Create a new project by manual creation.
     * Throw DuplicateProjectNameException when project name is duplicate for user uuid.
     *
     * @param createProjectRequest create project request
     * @param userId user uuid
     * @return New project
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public Project createNewProjectByManualCreation(CreateProjectRequest createProjectRequest,
                                                    UUID userId) {
        String projectName = createProjectRequest.getProjectName();
        String projectDescription = createProjectRequest.getProjectDescription();

        // Check whether project name has been belongs to this userId
        List<Project> projectsOwnedByUserId = this.projectRepository.findProjectsByUserId(userId);
        boolean invalidProjectName = projectsOwnedByUserId.stream().anyMatch(p -> p.getName().equals(projectName));
        if (invalidProjectName) {
            throw new DuplicateProjectNameException();
        }


        Project project = Project.builder()
            .userId(userId)
            .name(projectName)
            .description(projectDescription)
            .averageDuration(0)
            .cost(BigDecimal.ZERO)
            .lastUpdateTimestamp(LocalDateTime.now())
            .build();

        this.projectRepository.save(project);
        return project;
    }

    @Override
    public List<Project> getProjectByUserId(UUID userId) {
        return List.of();
    }

    @Override
    public Project getProjectByName(UUID userId,
                                    String projectName) {
        return null;
    }

    @Override
    public Project updateProjectAfterLogging(UUID userId,
                                             String projectName,
                                             BigDecimal costGeneratedFromThisLog,
                                             LocalDateTime logEndTimestamp,
                                             BigDecimal durationOfThisLog) {
        return null;
    }

    @Override
    public Project deleteProject(UUID userId,
                                 String projectName) {
        return null;
    }
}
