package com.supertrace.aitrace.service;

import com.supertrace.aitrace.auth.AuthRequest;
import com.supertrace.aitrace.auth.AuthResponse;

/** Sign in AITrace service
 *
 * @author dass90
 * @since 2025-11-21
 */
public interface AuthService<T extends AuthRequest, V extends AuthResponse> {
    String type();
    V authenticate(T request);
}
