package com.supertrace.aitrace.service;

import com.supertrace.aitrace.dto.step.LogStepRequest;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

public interface LogService {
    UUID logStep(@NotNull UUID userId, @NotNull LogStepRequest logStepRequest);
}
