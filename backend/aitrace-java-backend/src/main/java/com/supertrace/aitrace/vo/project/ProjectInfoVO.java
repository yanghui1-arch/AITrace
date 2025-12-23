package com.supertrace.aitrace.vo.project;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
public class ProjectInfoVO {

    @NotNull
    private Long projectId;

    @NotBlank
    private String projectName;

    private String description;

    @NotNull
    private Integer averageDuration;

    @NotNull
    private BigDecimal cost;

    @NotNull
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createdTimestamp;

    @NotNull
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime lastUpdateTimestamp;
}
