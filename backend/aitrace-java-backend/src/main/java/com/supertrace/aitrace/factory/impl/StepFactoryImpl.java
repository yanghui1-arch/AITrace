package com.supertrace.aitrace.factory.impl;

import com.supertrace.aitrace.domain.core.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.factory.StepFactory;
import org.springframework.stereotype.Component;

import java.util.Optional;
import java.util.UUID;

/**
 * Create step factory
 *
 * @author dass90
 * @since 2025-10-23
 */
@Component
public class StepFactoryImpl implements StepFactory {
    /**
     * Create a step from log step request
     *
     * @param request log step request DTO
     * @return step domain
     */
    @Override
    public Step createStep(LogStepRequest request) {
        return Step.builder()
                .id(UUID.fromString(request.getStepId()))
                .name(request.getStepName())
                .traceId(UUID.fromString(request.getTraceId()))
                .parentStepId(Optional.ofNullable(request.getParentStepId())
                        .map(UUID::fromString)
                        .orElse(null))
                .type(request.getStepType())
                .tags(request.getTags())
                .input(request.getInput())
                .output(request.getOutput())
                .errorInfo(request.getErrorInfo())
                .model(request.getModel())
                .usage(request.getUsage())
                .projectName(request.getProjectName())
                .startTime(request.getStartTime())
                .endTime(request.getEndTime())
                .build();
    }
}
