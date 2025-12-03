package com.supertrace.aitrace.service.application;

import java.util.Optional;
import java.util.UUID;

/**
 * Api key service
 * Offer generate api key, validate whether api key owned by user and get api key of a user.
 *
 * @author dass90
 * @since 2025-10-21
 */
public interface ApiKeyService {

    /**
     * Generate an api key and store it
     *
     * @param userId user uuid of apikey
     * @return api key
     */
    String generateAndStoreApiKey(UUID userId);

    /**
     * Judge if this api key is owned by user id.
     *
     * @param apiKey api key
     * @param userId user id
     * @return true if owned else false
     */
    boolean isApiKeyOwnedByUser(String apiKey, UUID userId);

    /**
     * Resolve user uuid from API key
     *
     * @param apiKey apikey
     * @return Optional user uuid
     */
    Optional<UUID> resolveUserIdFromApiKey(String apiKey);

    /**
     * Get a user latest api key.
     *
     * @param userId user id
     * @return a list of api keys owned by user id
     */
    Optional<String> getUserLatestApiKey(UUID userId);

    /**
     * Judge if the apikey exists in database
     *
     * @param apiKey api key
     * @return true if exists else false
     */
    boolean isApiKeyExist(String apiKey);

}
