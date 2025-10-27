package com.supertrace.aitrace.dto.step;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import jakarta.persistence.Column;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@Data
public class LogStepRequest {
    @NotNull
    private String projectName;

    @NotNull
    private String stepName;

    @NotNull
    private String stepId;

    @NotNull
    private String traceId;

    private String parentStepId;

    @NotNull
    @Pattern(regexp = "customized|llm_response|retrieve|tool",
            message = "step type must be one of `customized`, `llm_response`, `retrieve` and tool.")
    private String stepType;

    @NotNull
    private List<String> tags;

    private Map<String, Object> input;

    private Map<String, Object> output;

    private String errorInfo;

    private String model;

    private Map<String, Object> usage;

    @NotNull
    private LocalDateTime startTime;

    private LocalDateTime endTime;
}
