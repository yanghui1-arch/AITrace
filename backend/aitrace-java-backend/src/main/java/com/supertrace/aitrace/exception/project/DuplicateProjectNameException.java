package com.supertrace.aitrace.exception.project;

public class DuplicateProjectNameException extends RuntimeException {
    private static final String DUPLICATE_PROJECT_NAME = "Invalid to duplicate project name owed by a user.";

    public DuplicateProjectNameException() {
        super(DUPLICATE_PROJECT_NAME);
    }
}
