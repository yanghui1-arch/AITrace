package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.core.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.factory.StepFactory;
import com.supertrace.aitrace.repository.StepRepository;
import com.supertrace.aitrace.service.StepService;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

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

        // 1. using factory to build a step domain
        Step step = stepFactory.createStep(logStepRequest);

        // 2. save step
        stepRepository.saveAndFlush(step);

        // 3. logger

        // 4. return step id
        return step.getId();
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public List<Step> getAllSteps(@NotBlank String projectName) {
       return this.stepRepository.findByProjectName(projectName);
    }
}
