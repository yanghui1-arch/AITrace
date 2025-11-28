package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.ApiKeyService;
import com.supertrace.aitrace.utils.ApiKeyUtils;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/api/apikey")
public class APIKeyController {

    private final ApiKeyService apiKeyService;

    @Autowired
    public APIKeyController(ApiKeyService apiKeyService) {
        this.apiKeyService = apiKeyService;
    }

    @GetMapping("/get")
    public ResponseEntity<APIResponse<String>> getAPIKey(HttpServletRequest request) {
        try {
            UUID userId = (UUID) request.getAttribute("userId");
            Optional<String> apiKey = this.apiKeyService.getUserLatestApiKey(userId);
            return apiKey
                .map(ApiKeyUtils::concealApiKey)
                .map(s -> ResponseEntity.ok(APIResponse.success(s)))
                .orElseGet(() -> ResponseEntity.notFound().build());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/get_complete_apikey")
    public ResponseEntity<APIResponse<String>> getCompleteAPIKey(HttpServletRequest request) {
        try {
            UUID userId = (UUID) request.getAttribute("userId");
            Optional<String> apiKey = this.apiKeyService.getUserLatestApiKey(userId);
            return apiKey
                .map(s -> ResponseEntity.ok(APIResponse.success(s)))
                .orElseGet(() -> ResponseEntity.notFound().build());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }

    @PostMapping("/change")
    public ResponseEntity<APIResponse<String>> changeApiKey(HttpServletRequest request) {
        try {
            UUID userId = (UUID) request.getAttribute("userId");
            String apiKey = this.apiKeyService.generateAndStoreApiKey(userId);
            return ResponseEntity.ok(APIResponse.success(ApiKeyUtils.concealApiKey(apiKey), "Change another AITrace API key successfully."));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
