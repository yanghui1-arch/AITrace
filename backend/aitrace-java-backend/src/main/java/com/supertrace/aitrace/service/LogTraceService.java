package com.supertrace.aitrace.service;

import com.supertrace.aitrace.dto.trace.LogTraceRequest;

import java.util.UUID;

/**
 * Log trace service
 *
 * @author dass90
 * @since 2025-10-24
 */
public interface LogTraceService {
    /**
     * store trace into the database
     * Trace is the one generation in the complete workflow of agent
     *
     * @param logTraceRequest log trace request
     * @return step id
     */
    UUID logTrace(LogTraceRequest logTraceRequest);
}
