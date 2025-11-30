package com.supertrace.aitrace.vo.project;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
public class ProjectInfoVO {

    @NotBlank
    private String projectName;

    private String description;

    @NotNull
    private Integer averageDuration;

    @NotNull
    private BigDecimal cost;

    @NotNull
    private LocalDateTime createdTimestamp;

    @NotNull
    private LocalDateTime lastUpdateTimestamp;
}
