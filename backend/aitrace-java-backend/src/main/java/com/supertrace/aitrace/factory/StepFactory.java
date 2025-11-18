package com.supertrace.aitrace.factory;

import com.supertrace.aitrace.domain.core.step.Step;
import com.supertrace.aitrace.dto.step.LogStepRequest;

public interface StepFactory {
    Step createStep(LogStepRequest request);
}
