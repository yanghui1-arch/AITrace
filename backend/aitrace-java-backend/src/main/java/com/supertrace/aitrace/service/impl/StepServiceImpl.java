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

import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Stream;

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

        Step newStep = null;
        // 1. merge or create step
        UUID stepId = UUID.fromString(logStepRequest.getStepId());
        Optional<Step> dbStep = stepRepository.findById(stepId);
        if (dbStep.isPresent()) {
            // update
            Step step = dbStep.get();
            newStep = this.mergeStepWithRequest(step, logStepRequest);
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

    /**
     * Update step
     * It's a little difficult to manage all outputs and usage in the sdk
     * Because it's complex to know when callers consumes openai.Stream.
     * Therefore, transfer the complexity of sdk to the server.
     * Note: dbstep and logStepRequest id should be the same.
     *
     * @param dbStep: step from database
     * @param logStepRequest: log step request
     * @return
     */
    public Step mergeStepWithRequest(@NotNull Step dbStep, @NotNull LogStepRequest logStepRequest) {
        Step mergedStep = null;

        // merge tags first
        List<String> oldTags = dbStep.getTags();
        List<String> newTags = logStepRequest.getTags();
        List<String> mergedTags = Stream.concat(newTags.stream(), oldTags.stream())
                .filter(Objects::nonNull)
                .distinct()
                .toList();

        // merge outputs


        return mergedStep;
    }
}
