package com.supertrace.aitrace.registry;

import com.supertrace.aitrace.auth.AuthRequest;
import com.supertrace.aitrace.auth.AuthResponse;
import com.supertrace.aitrace.service.application.AuthService;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Authentication service registry
 * All AuthServiceImpl classes which implement AuthService will be created an instance in the AuthServiceRegistry.
 * Caller pass an authentication name and get an AuthService to use.
 *
 * @author dass90
 * @since 2025/11/22
 */
@Component
@RequiredArgsConstructor
public class AuthServiceRegistry {
    private final List<AuthService<?, ?>> authServices;

    private Map<String, AuthService<?, ?>> authServiceMap;

    @PostConstruct
    public void init() {
        this.authServiceMap = authServices.stream()
            .collect(Collectors.toMap(AuthService::type, s -> s));
    }

    @SuppressWarnings("unchecked")
    public <T extends AuthRequest, V extends AuthResponse> AuthService<T, V> getService(String type) {
        AuthService<?, ?> authService = Optional.ofNullable(authServiceMap.get(type))
            .orElseThrow(
                () -> new IllegalArgumentException("Unsupported authentication type: " + type)
            );
        return (AuthService<T, V>) authService;
    }
}
