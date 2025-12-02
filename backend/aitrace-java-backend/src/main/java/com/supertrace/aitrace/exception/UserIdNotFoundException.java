package com.supertrace.aitrace.exception;

public class UserIdNotFoundException extends RuntimeException {
    private static final long UNAUTHORIZED = 404;
    private static final String NOT_FOUND_MESSAGE = "Failed to find userId.";

    public UserIdNotFoundException() {
        super(NOT_FOUND_MESSAGE);
    }
}
