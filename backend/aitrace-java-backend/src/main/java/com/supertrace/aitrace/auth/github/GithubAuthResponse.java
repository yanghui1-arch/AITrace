package com.supertrace.aitrace.auth.github;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import com.supertrace.aitrace.auth.AuthResponse;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GithubAuthResponse implements AuthResponse {
    @NotNull
    private Long id;

    @NotNull
    @Email
    private String email;

    private String avatarUrl;

    private String name;
}
