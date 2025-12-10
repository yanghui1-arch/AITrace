package com.supertrace.aitrace.repository;

import com.supertrace.aitrace.domain.auth.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
    List<User> findUserById(UUID id);
}
