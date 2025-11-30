package com.supertrace.aitrace.dto.project;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class CreateProjectRequest {
    @NotBlank
    private String projectName;

    private String projectDescription;
}
