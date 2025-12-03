package com.supertrace.aitrace.service.application;

import com.supertrace.aitrace.dto.step.LogStepRequest;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

public interface LogService {
    UUID logStep(@NotNull UUID userId, @NotNull LogStepRequest logStepRequest);

    UUID logTrace(@NotNull UUID userId, @NotNull LogTraceRequest logTraceRequest);
}
