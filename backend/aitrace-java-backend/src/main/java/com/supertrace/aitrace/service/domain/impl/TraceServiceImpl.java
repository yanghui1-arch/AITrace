package com.supertrace.aitrace.service.domain.impl;

import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import com.supertrace.aitrace.factory.TraceFactory;
import com.supertrace.aitrace.repository.TraceRepository;
import com.supertrace.aitrace.service.domain.TraceService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class TraceServiceImpl implements TraceService {

    private final TraceRepository traceRepository;
    private final TraceFactory traceFactory;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public UUID createTrace(LogTraceRequest logTraceRequest, Long projectId) {
        // 1. using factory to build a trace
        Trace trace = traceFactory.createTrace(logTraceRequest, projectId);
        // 2. save trace
        traceRepository.saveAndFlush(trace);
        // 3. logger
        // 4. return trace id
        return trace.getId();
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public List<Trace> getTrace(String projectName) {
        return this.traceRepository.findByProjectName(projectName);
    }
}
