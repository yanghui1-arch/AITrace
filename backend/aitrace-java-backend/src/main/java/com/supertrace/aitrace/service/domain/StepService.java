package com.supertrace.aitrace.service.domain;

import com.supertrace.aitrace.domain.core.step.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;

import java.util.List;
import java.util.UUID;

/**
 * Log step service
 *
 * @author dass90
 * @since 2025-10-23
 */
public interface StepService {
    /**
     * Store step into the database
     * If step id is not in the db create one and store it else update it.
     *
     * @param userId user uuid
     * @param logStepRequest log step request
     * @return step id
     */
    UUID logStep(UUID userId, LogStepRequest logStepRequest, Long projectId);

    /**
     * get all steps of a project which is owned by userId
     *
     * @param projectId project id.
     * @return all steps
     */
    List<Step> findStepsByProjectId(Long projectId);
}
