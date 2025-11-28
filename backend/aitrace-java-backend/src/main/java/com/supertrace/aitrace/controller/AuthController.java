package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.auth.github.GithubAuthRequest;
import com.supertrace.aitrace.auth.github.GithubAuthResponse;
import com.supertrace.aitrace.domain.auth.AuthPlatform;
import com.supertrace.aitrace.domain.auth.User;
import com.supertrace.aitrace.domain.auth.UserAuth;
import com.supertrace.aitrace.registry.AuthServiceRegistry;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.ApiKeyService;
import com.supertrace.aitrace.service.AuthService;
import com.supertrace.aitrace.service.UserService;
import com.supertrace.aitrace.utils.JwtUtil;
import com.supertrace.aitrace.vo.AuthVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final JwtUtil jwtUtil;
    private final AuthServiceRegistry authServiceRegistry;
    private final UserService userService;
    private final ApiKeyService apiKeyService;

    @Autowired
    public AuthController(JwtUtil jwtUtil, AuthServiceRegistry authServiceRegistry, UserService userService, ApiKeyService apiKeyService) {
        this.jwtUtil = jwtUtil;
        this.authServiceRegistry = authServiceRegistry;
        this.userService = userService;
        this.apiKeyService = apiKeyService;
    }

    /**
     * Authentication while using GitHub to sign in AITrace
     * The process of AITrace authentication (using GitHub) is passing GitHub authentication first and then check whether existing GitHub account id.
     * It means a new user with GitHub sign in AITrace if GitHub account id is not existed.
     * Else it's a registered user of AITrace.
     *
     * @param code GitHub code
     * @param state GitHub state
     * @return AITrace user uuid and jwt token
     */
    @GetMapping("/github/callback")
    public ResponseEntity<APIResponse<AuthVO>> authenticate(@RequestParam("code") String code, @RequestParam(value = "state", required = false) String state) {
        try {
            AuthService<GithubAuthRequest, GithubAuthResponse> authService = this.authServiceRegistry.getService("github");
            GithubAuthResponse response = authService.authenticate(GithubAuthRequest.builder().code(code).build());
            Optional<UserAuth> userAuth = this.userService.findUserAuthByIdentifier(response.getId().toString());
            // userId and responseMessage is both get the value in this situation.
            UUID userId;
            String responseMessage;
            if (userAuth.isPresent()) {
                userId = userAuth.get().getUserId();
                responseMessage = "GitHub authenticate successfully.";
            } else {
                User user = this.userService.createUser(
                    response.getName(),
                    response.getEmail(),
                    response.getAvatarUrl(),
                    AuthPlatform.GitHub,
                    String.valueOf(response.getId())
                );
                userId = user.getId();
                // New user is created, allocate an apikey for him
                this.apiKeyService.generateAndStoreApiKey(userId);
                responseMessage = "New user with using GitHub authentication is registered successfully.";
            }
            String jwtToken = this.jwtUtil.generateToken(userId);
            return ResponseEntity.ok(
                APIResponse.success(AuthVO.builder().userId(userId).token(jwtToken).build(), responseMessage)
            );
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
