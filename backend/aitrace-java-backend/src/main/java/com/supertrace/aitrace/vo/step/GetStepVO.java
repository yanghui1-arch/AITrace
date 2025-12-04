package com.supertrace.aitrace.vo.step;

import com.supertrace.aitrace.domain.core.step.StepOutput;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Data
@Builder
public class GetStepVO {
    private UUID id;

    private UUID parentStepId;

    @NotNull
    private String name;

    @NotBlank
    private String type;

    @NotNull
    private List<String> tags;

    private Map<String, Object> input;

    private StepOutput output;

    private String errorInfo;

    private String model;

    private Map<String, Object> usage;

    private LocalDateTime startTime;

    private LocalDateTime endTime;

}
