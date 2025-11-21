package com.supertrace.aitrace.auth.github;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@Data
public class GithubUser {
    private String login;
    private Long id;
    private String avatarUrl;
    private String htmlUrl;
    private String name;
    private String email;
}
