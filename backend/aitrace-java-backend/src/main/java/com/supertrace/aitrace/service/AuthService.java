package com.supertrace.aitrace.service;

import com.supertrace.aitrace.auth.AuthRequest;

/** Sign in AITrace service
 *
 * @author dass90
 * @since 2025-11-21
 */
public interface AuthService<T extends AuthRequest> {
    String type();
    boolean authenticate(T request);
}
