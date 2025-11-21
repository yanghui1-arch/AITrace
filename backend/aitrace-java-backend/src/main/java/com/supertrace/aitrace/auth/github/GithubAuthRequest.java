package com.supertrace.aitrace.auth.github;

import com.supertrace.aitrace.auth.AuthRequest;
import lombok.Data;

@Data
public class GithubAuthRequest implements AuthRequest {
    private String code;
}
