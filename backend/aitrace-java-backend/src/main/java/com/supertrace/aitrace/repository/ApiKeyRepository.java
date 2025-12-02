package com.supertrace.aitrace.repository;

import com.supertrace.aitrace.domain.ApiKey;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ApiKeyRepository extends JpaRepository<ApiKey, UUID> {
    List<ApiKey> findApiKeyByUserId(UUID userId);
    List<ApiKey> findApiKeyByKey(String apiKey);

    @Query("select apikey.userId from ApiKey as apikey where apikey.key = :apiKey")
    Optional<UUID> findUserIdByKey(@Param("apiKey") String apiKey);
}
