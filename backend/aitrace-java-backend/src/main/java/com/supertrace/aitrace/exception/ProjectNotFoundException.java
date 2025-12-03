package com.supertrace.aitrace.exception;

public class ProjectNotFoundException extends RuntimeException {
    private static final long NOT_FOUND = 404;

    public ProjectNotFoundException(String message) {
        super(message);
    }
}
