package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.auth.github.GithubAuthRequest;
import com.supertrace.aitrace.auth.github.GithubAuthResponse;
import com.supertrace.aitrace.domain.auth.AuthPlatform;
import com.supertrace.aitrace.domain.auth.User;
import com.supertrace.aitrace.domain.auth.UserAuth;
import com.supertrace.aitrace.exception.UserIdNotFoundException;
import com.supertrace.aitrace.registry.AuthServiceRegistry;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.application.ApiKeyService;
import com.supertrace.aitrace.service.application.AuthService;
import com.supertrace.aitrace.service.domain.UserService;
import com.supertrace.aitrace.utils.JwtUtil;
import com.supertrace.aitrace.vo.AuthVO;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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
     * It is worth noting that GitHub's username and login name are two different things. Here, the priority is to check if a username exists;
     * if it does, it is used as the username. If username is null, then the login name is used as the username.
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
            // user and responseMessage is both get the value in this situation.
            User user;
            String responseMessage;
            if (userAuth.isPresent()) {
                UUID userId = userAuth.get().getUserId();
                user = this.userService.findUserByUserId(userId).orElseThrow(UserIdNotFoundException::new);
                responseMessage = "GitHub authenticate successfully.";
            } else {
                String userName = Optional.ofNullable(response.getName()).orElse(response.getLogin());
                user = this.userService.createUser(
                    userName,
                    response.getEmail(),
                    response.getAvatarUrl(),
                    AuthPlatform.GitHub,
                    String.valueOf(response.getId())
                );
                // New user is created, allocate an apikey for him
                this.apiKeyService.generateAndStoreApiKey(user.getId());
                responseMessage = "New user with using GitHub authentication is registered successfully.";
            }
            String jwtToken = this.jwtUtil.generateToken(user.getId());
            return ResponseEntity.ok(
                APIResponse.success(
                    AuthVO.builder()
                        .userName(user.getUsername())
                        .avatar(user.getAvatar())
                        .token(jwtToken)
                        .build(),
                    responseMessage
                )
            );
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/me")
    public ResponseEntity<APIResponse<AuthVO>> me(HttpServletRequest request) {
        try {
            String token = request.getHeader("AT-token");
            UUID userId = (UUID) request.getAttribute("userId");
            User user = this.userService.findUserByUserId(userId).orElseThrow(UserIdNotFoundException::new);
            return ResponseEntity.ok(APIResponse.success(AuthVO.builder().userName(user.getUsername()).avatar(user.getAvatar()).token(token).build()));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
