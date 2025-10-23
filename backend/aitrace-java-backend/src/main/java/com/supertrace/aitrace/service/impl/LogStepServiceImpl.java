package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.core.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.repository.StepRepository;
import com.supertrace.aitrace.service.LogStepService;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class LogStepServiceImpl implements LogStepService {

    private final StepRepository stepRepository;

    /**
     * Validate request and persist step.
     *
     * @param logStepRequest log step request
     * @return step id
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public UUID logStep(@NotNull LogStepRequest logStepRequest) {

        // 1. using factory to build a step domain
        Step step = new Step();
        if (logStepRequest.getStepId() != null) {
            step.setId(UUID.fromString(logStepRequest.getStepId()));
        }
        if (logStepRequest.getParentStepId() != null) {
            step.setParentStepId(UUID.fromString(logStepRequest.getParentStepId()));
        }
        if (logStepRequest.getTraceId() != null) {
            step.setTraceId(UUID.fromString(logStepRequest.getTraceId()));
        }

        step.setName(logStepRequest.getStepName());
        step.setProjectName(logStepRequest.getProjectName());
        step.setModel(logStepRequest.getModel());
        step.setInput(logStepRequest.getInput());
        step.setOutput(logStepRequest.getOutput());
        step.setTags(logStepRequest.getTags());
        step.setErrorInfo(logStepRequest.getErrorInfo());
        step.setType(logStepRequest.getStepType());
        step.setUsage(logStepRequest.getUsage());

        // 2. save step
        stepRepository.saveAndFlush(step);

        // 3. logger

        // 4. return step id
        return step.getId();
    }
}
