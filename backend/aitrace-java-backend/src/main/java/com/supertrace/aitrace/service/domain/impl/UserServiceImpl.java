package com.supertrace.aitrace.service.domain.impl;

import com.supertrace.aitrace.domain.auth.AuthPlatform;
import com.supertrace.aitrace.domain.auth.User;
import com.supertrace.aitrace.domain.auth.UserAuth;
import com.supertrace.aitrace.repository.UserAuthRepository;
import com.supertrace.aitrace.repository.UserRepository;
import com.supertrace.aitrace.service.domain.UserService;
import jakarta.transaction.Transactional;
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
    public User createUser(String username,
                           String email,
                           String avatar,
                           AuthPlatform authPlatform,
                           String identifier) {
        User user = User.builder()
            .username(username)
            .email(email)
            .avatar(avatar)
            .build();
        userRepository.save(user);

        UserAuth userAuth = UserAuth.builder()
            .userId(user.getId())
            .authType(authPlatform)
            .identifier(identifier)
            .build();

        userAuthRepository.save(userAuth);

        return user;
    }

    @Override
    public Optional<UserAuth> findUserAuthByIdentifier(String identifier) {
        return this.userAuthRepository.findUserAuthByIdentifier(identifier);
    }

}
