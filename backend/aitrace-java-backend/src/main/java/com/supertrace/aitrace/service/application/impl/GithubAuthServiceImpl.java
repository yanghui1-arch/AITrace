package com.supertrace.aitrace.service.application.impl;

import com.supertrace.aitrace.auth.github.GithubAuthRequest;
import com.supertrace.aitrace.auth.github.GithubAuthResponse;
import com.supertrace.aitrace.auth.github.GithubTokenResponse;
import com.supertrace.aitrace.service.application.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.Optional;


@Service
@RequiredArgsConstructor
public class GithubAuthServiceImpl implements AuthService<GithubAuthRequest, GithubAuthResponse> {
    @Value("${github.client-id}")
    private String clientId;

    @Value("${github.client-secret}")
    private String clientSecret;

    @Value("${github.redirect-url}")
    private String redirectUri;

    private final WebClient webClient = WebClient.create();

    @Override
    public String type() {
        return "github";
    }

    /**
     * Authenticate GitHub code from fronted
     *
     * @param request GitHub authentication request
     * @return GithubAuthResponse
     */
    @Override
    public GithubAuthResponse authenticate(GithubAuthRequest request) {
        String code = request.getCode();
        String accessToken = this.getAccessToken(code)
            .orElseThrow(() -> new RuntimeException("No access token"));
        return this.getGithubUser(accessToken);
    }

    /**
     * Get user GitHub access token
     *
     * @param code code
     * @return Optional GitHub access token
     * @throws RuntimeException When GitHub is down
     */
    private Optional<String> getAccessToken(String code) {
        var form = BodyInserters
            .fromFormData("client_id", clientId)
            .with("client_secret", clientSecret)
            .with("code", code)
            .with("redirect_uri", redirectUri);
        GithubTokenResponse response =  webClient.post()
            .uri("https://github.com/login/oauth/access_token")
            .header("Accept", "application/json")
            .body(form)
            .retrieve()
            .onStatus(HttpStatusCode::isError,
                res -> Mono.error(
                    new RuntimeException("Failed to request GitHub OAuth: " + res.statusCode())
                )
            )
            .bodyToMono(GithubTokenResponse.class)
            .block();
        return Optional.ofNullable(response)
            .map(GithubTokenResponse::getAccessToken);
    }

    /**
     * Get GitHub user with access token
     *
     * @param accessToken user access token
     * @return GithubAuthResponse
     * @throws RuntimeException When access token is expired or wrong.
     */
    private GithubAuthResponse getGithubUser(String accessToken) {
        return webClient.get()
            .uri("https://api.github.com/user")
            .header("Authorization", "Bearer " + accessToken)
            .retrieve()
            .onStatus(HttpStatusCode::is4xxClientError,
                res -> Mono.error(
                    new RuntimeException("Failed to get user information with github access token: " + res.statusCode())
                )
            )
            .bodyToMono(GithubAuthResponse.class)
            .block();
    }
}
