package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.auth.AuthPlatform;
import com.supertrace.aitrace.domain.auth.User;
import com.supertrace.aitrace.domain.auth.UserAuth;
import com.supertrace.aitrace.repository.UserAuthRepository;
import com.supertrace.aitrace.repository.UserRepository;
import com.supertrace.aitrace.service.UserService;
import jakarta.transaction.Transactional;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final UserAuthRepository userAuthRepository;

    @Override
    @Transactional(rollbackOn = Exception.class)
    public User createUser(@NotNull String username,
                           @NotNull String email,
                           @NotNull String avatar,
                           @NotNull AuthPlatform authPlatform,
                           @NotNull String identifier) {
        User user = User.builder()
            .username(username)
            .email(email)
            .avatar(avatar)
            .build();

        UserAuth userAuth = UserAuth.builder()
            .userId(user.getId())
            .authType(authPlatform)
            .identifier(identifier)
            .build();

        userRepository.save(user);
        userAuthRepository.save(userAuth);

        return user;
    }

    @Override
    public Optional<UserAuth> findUserAuthByIdentifier(String identifier) {
        return this.userAuthRepository.findUserAuthByIdentifier(identifier);
    }

}
