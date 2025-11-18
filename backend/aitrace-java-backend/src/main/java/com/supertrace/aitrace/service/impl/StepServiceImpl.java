package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.core.step.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.factory.StepFactory;
import com.supertrace.aitrace.repository.StepRepository;
import com.supertrace.aitrace.service.StepService;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Service
@RequiredArgsConstructor
public class StepServiceImpl implements StepService {

    private final StepRepository stepRepository;
    private final StepFactory stepFactory;

    /**
     * Validate request and persist step.
     *
     * @param logStepRequest log step request
     * @return step id
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public UUID logStep(@NotNull LogStepRequest logStepRequest) {

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
            newStep = stepFactory.createStep(logStepRequest);
        }

        // 2. save step
        stepRepository.saveAndFlush(newStep);

        // 3. logger

        // 4. return step id
        return newStep.getId();
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public List<Step> getAllSteps(@NotBlank String projectName) {
       return this.stepRepository.findByProjectName(projectName);
    }
}
