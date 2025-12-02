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
import java.util.Optional;
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
    @Transactional(rollbackFor = Exception.class)
    public Project createNewProjectByProgram(String projectName,
                                             UUID userId) {
        List<Project> projectsOwnedByUserId = this.projectRepository.findProjectsByUserId(userId);
        boolean invalidProjectName = projectsOwnedByUserId.stream().anyMatch(p -> p.getName().equals(projectName));
        if (invalidProjectName) {
            throw new DuplicateProjectNameException();
        }
        Project project = Project.builder()
            .userId(userId)
            .name(projectName)
            .averageDuration(0)
            .cost(BigDecimal.ZERO)
            .lastUpdateTimestamp(LocalDateTime.now())
            .build();
        this.projectRepository.save(project);
        return project;
    }

    @Override
    public List<Project> getProjectsByUserId(UUID userId) {
        return this.projectRepository.findProjectsByUserId(userId);
    }

    @Override
    public Optional<Project> getProjectByUserIdAndName(UUID userId, String projectName) {
        List<Project> projectsOwnedByUserId = this.projectRepository.findProjectsByUserId(userId);
        return projectsOwnedByUserId.stream()
            .filter(p -> p.getName().equals(projectName))
            .findFirst();
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
        List<Project> projectsOwnedByUserId = this.projectRepository.findProjectsByUserId(userId);
        if (projectsOwnedByUserId.isEmpty()) {
            throw new IllegalArgumentException("No projects owned by this user: " + userId);
        } else {
            Project projectToDelete = projectsOwnedByUserId.stream()
                .filter(p -> p.getName().equals(projectName))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Project not found"));
            this.projectRepository.deleteById(projectToDelete.getId());
            return projectToDelete;
        }
    }
}
