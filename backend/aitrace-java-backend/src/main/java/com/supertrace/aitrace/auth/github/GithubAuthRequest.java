package com.supertrace.aitrace.auth.github;

import com.supertrace.aitrace.auth.AuthRequest;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class GithubAuthRequest implements AuthRequest {
    private String code;
}
