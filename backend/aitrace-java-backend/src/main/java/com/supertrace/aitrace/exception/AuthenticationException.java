package com.supertrace.aitrace.exception;

public class AuthenticationException extends RuntimeException {
    private static final long UNAUTHORIZED = 401;
    private static final String UNAUTHORIZED_MESSAGE = "Unauthorized for invalid AITrace API key";

    public AuthenticationException() {
        super(UNAUTHORIZED_MESSAGE);
    }
}
