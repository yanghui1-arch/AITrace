package com.supertrace.aitrace.service.application.impl;

import com.supertrace.aitrace.domain.core.step.Step;
import com.supertrace.aitrace.service.application.DeleteService;
import com.supertrace.aitrace.service.domain.StepService;
import com.supertrace.aitrace.service.domain.TraceService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class DeleteServiceImpl implements DeleteService {
    private final StepService stepService;
    private final TraceService traceService;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public List<UUID> deleteTracesAndRelatedStepsByTraceIds(List<UUID> traceIdsToDelete) {
        List<UUID> relatedStepsIdByTraceIds = traceIdsToDelete.stream()
            .flatMap(
                traceId -> this.stepService.findStepsByTraceId(traceId).stream().map(Step::getId)
            )
            .toList();
        this.stepService.deleteStepsByStepUUID(relatedStepsIdByTraceIds);
        this.traceService.deleteTraceByTraceId(traceIdsToDelete);
        return traceIdsToDelete;
    }
}
