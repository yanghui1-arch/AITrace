package com.supertrace.aitrace.service;

import com.supertrace.aitrace.domain.Project;
import com.supertrace.aitrace.dto.project.CreateProjectRequest;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

public interface ProjectService {
    /**
     * Create a new project and store it into database.
     * It's forbidden to create the same project name under a user and should be implemented in this function.
     *
     * @param createProjectRequest create project request
     * @param userId user uuid
     * @return Project
     */
    Project createNewProjectByManualCreation(CreateProjectRequest createProjectRequest, UUID userId);

    /**
     * Get all projects of user uuid
     *
     * @param userId user uuid
     * @return List of projects owned by user uuid
     */
    List<Project> getProjectsByUserId(UUID userId);

    /**
     * Get project all information of project name owned by user uuid
     *
     * @param userId user uuid
     * @param projectName project name
     * @return Project
     */
    Project getProjectByName(UUID userId, String projectName);

    /**
     * Update project after logging.
     * Offer parameters are all raw data of this log. Complex calculation is implemented in this function.
     * Average calculation is implemented using stream update method.
     *
     * @param userId user uuid
     * @param projectName project name
     * @param costGeneratedFromThisLog LLM cost generation from this log
     * @param logEndTimestamp log end timestamp
     * @param durationOfThisLog duration of this log
     * @return Updated project
     */
    Project updateProjectAfterLogging(UUID userId, String projectName, BigDecimal costGeneratedFromThisLog, LocalDateTime logEndTimestamp, BigDecimal durationOfThisLog);

    /**
     * Delete a project of a user by project name
     *
     * @param userId user uuid which want to delete
     * @param projectName project name to delete
     * @return Project to delete
     */
    Project deleteProject(UUID userId, String projectName);
}
