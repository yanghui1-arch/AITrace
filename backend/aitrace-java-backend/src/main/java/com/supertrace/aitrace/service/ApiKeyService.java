package com.supertrace.aitrace.service;

import java.util.List;
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
     * Generate an api key
     *
     * @return api key
     */
    String generateApiKey();

    /**
     * Judge if this api key is owned by user id.
     *
     * @param apiKey api key
     * @param userId user id
     * @return true if owned else false
     */
    boolean isApiKeyOwnedByUser(String apiKey, UUID userId);

    /**
     * Get a user all api keys.
     * Get all api keys owned by a user no matter it's deprecated
     *
     * @param userId user id
     * @return a list of api keys owned by user id
     */
    List<String> getUserApiKeys(UUID userId);

}
