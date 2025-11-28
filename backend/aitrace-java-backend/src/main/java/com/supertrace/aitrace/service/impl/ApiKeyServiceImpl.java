package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.ApiKey;
import com.supertrace.aitrace.repository.ApiKeyRepository;
import com.supertrace.aitrace.service.ApiKeyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class ApiKeyServiceImpl implements ApiKeyService {

    private static final String PREFIX = "at-";

    private final ApiKeyRepository apiKeyRepository;

    @Autowired
    public ApiKeyServiceImpl(ApiKeyRepository apiKeyRepository) {
        this.apiKeyRepository = apiKeyRepository;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public String generateAndStoreApiKey(UUID userId) {
        String uuid = UUID.randomUUID().toString().replace("-", "");
        String apiKey = PREFIX + uuid;
        List<ApiKey> oldKey = this.apiKeyRepository.findApiKeyByUserId(userId);
        if (!oldKey.isEmpty()) {
            this.apiKeyRepository.deleteAll(oldKey);
        }

        ApiKey newKey = ApiKey.builder()
            .key(apiKey)
            .userId(userId)
            .build();

        this.apiKeyRepository.save(newKey);
        return apiKey;
    }

    @Override
    public boolean isApiKeyOwnedByUser(String apiKey,
                                       UUID userId) {
        return false;
    }

    @Override
    public Optional<String> getUserLatestApiKey(UUID userId) {
        List<ApiKey> userApiKeys = this.apiKeyRepository.findApiKeyByUserId(userId);
        return userApiKeys.stream()
            .findFirst()
            .map(ApiKey::getKey);
    }

    @Override
    public boolean isApiKeyExist(String apiKey) {
        List<ApiKey> dbApiKeys = this.apiKeyRepository.findApiKeyByKey(apiKey);
        return !dbApiKeys.isEmpty() && dbApiKeys.stream().anyMatch(a -> a.getKey().equals(apiKey));
    }
}
