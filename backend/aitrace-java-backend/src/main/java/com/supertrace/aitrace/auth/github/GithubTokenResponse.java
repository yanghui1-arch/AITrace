package com.supertrace.aitrace.auth.github;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@Data
public class GithubTokenResponse {
    private String accessToken;
    private String tokenType;
    private String expiresIn;
}
