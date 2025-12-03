package com.supertrace.aitrace.service.domain;

import com.supertrace.aitrace.domain.auth.AuthPlatform;
import com.supertrace.aitrace.domain.auth.User;
import com.supertrace.aitrace.domain.auth.UserAuth;
import jakarta.transaction.Transactional;

import java.util.Optional;

public interface UserService {
    /**
     * Create a user in users and user_auth tables
     *
     * @param username username
     * @param email email
     * @param authPlatform authentication platform
     * @param identifier authentication platform identifier
     * @return User domain in users table
     */
    @Transactional(rollbackOn = Exception.class)
    User createUser(String username, String email, String avatar, AuthPlatform authPlatform, String identifier);

    /**
     * Find user with identifier
     *
     * @param identifier authentication platform identifier
     * @return Optional UserAuth
     */
    Optional<UserAuth> findUserAuthByIdentifier(String identifier);
}
