package com.supertrace.aitrace.service;

import com.supertrace.aitrace.domain.core.Step;
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
     * store step into the database
     *
     * @param logStepRequest log step request
     * @return step id
     */
    UUID logStep(LogStepRequest logStepRequest);

    /**
     * get all steps of a project
     *
     * @param projectName a project name
     * @return all steps
     */
    List<Step> getAllSteps(String projectName);
}
