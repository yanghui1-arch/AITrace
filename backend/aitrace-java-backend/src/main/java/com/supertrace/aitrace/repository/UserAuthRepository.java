package com.supertrace.aitrace.repository;

import com.supertrace.aitrace.domain.auth.UserAuth;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserAuthRepository extends JpaRepository<UserAuth, UUID> {
    Optional<UserAuth> findUserAuthByIdentifier(String identifier);
}
