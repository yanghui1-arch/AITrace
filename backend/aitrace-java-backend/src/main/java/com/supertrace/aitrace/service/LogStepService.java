package com.supertrace.aitrace.service;

import com.supertrace.aitrace.dto.step.LogStepRequest;

import java.util.UUID;

/**
 * Log step service
 *
 * @author dass90
 * @since 2025-10-23
 */
public interface LogStepService {
    /**
     * store step into the database
     *
     * @param logStepRequest log step request
     * @return step id
     */
    UUID logStep(LogStepRequest logStepRequest);
}
