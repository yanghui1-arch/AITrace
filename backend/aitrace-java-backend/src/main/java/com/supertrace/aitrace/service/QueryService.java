package com.supertrace.aitrace.service;

import com.supertrace.aitrace.domain.core.step.Step;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.util.List;
import java.util.UUID;

public interface QueryService {
    /**
     * Get all steps of project which is owned by user uuid.
     * @param userId user uuid
     * @param projectName project name
     * @return All steps.
     */
    List<Step> getSteps(@NotNull UUID userId, @NotBlank String projectName);
}
