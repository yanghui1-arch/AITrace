package com.supertrace.aitrace.service.domain;

import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import org.springframework.data.domain.Page;

import java.util.List;
import java.util.UUID;

/**
 * Log trace service
 *
 * @author dass90
 * @since 2025-10-24
 */
public interface TraceService {
    /**
     * store trace into the database
     * Trace is the one generation in the complete workflow of agent
     *
     * @param logTraceRequest log trace request
     * @param projectId project id which trace belongs to
     * @return step id
     */
    UUID createTrace(LogTraceRequest logTraceRequest, Long projectId);

    /**
     * Get all traces given a project Id
     *
     * @param projectId project id
     * @param page current page
     * @param pageSize page size
     * @return all traces
     */
    Page<Trace> getTracesByProjectId(Long projectId, int page, int pageSize);

    /**
     * Delete trace by trace id
     * @param traceIdsToDelete trace ids to delete
     * @return a list of uuid to delete.
     */
    List<UUID> deleteTraceByTraceId(List<UUID> traceIdsToDelete);
}
