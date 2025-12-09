package com.supertrace.aitrace.service.application;

import java.util.List;
import java.util.UUID;

public interface DeleteService {
    /**
     * Delete trace and related steps by trace ids.
     * It will do two things. One is to find the steps belongs to trace id and then delete them. Second is to delete the trace.
     * @param traceIdsToDelete trace ids to delete.
     * @return a list of trace ids to delete.
     */
    List<UUID> deleteTracesAndRelatedStepsByTraceIds(List<UUID> traceIdsToDelete);
}
