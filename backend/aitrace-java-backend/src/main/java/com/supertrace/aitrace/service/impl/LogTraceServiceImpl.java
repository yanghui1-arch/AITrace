package com.supertrace.aitrace.service.impl;

import com.supertrace.aitrace.domain.core.Step;
import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import com.supertrace.aitrace.factory.TraceFactory;
import com.supertrace.aitrace.repository.TraceRepository;
import com.supertrace.aitrace.service.LogTraceService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class LogTraceServiceImpl implements LogTraceService {

    private final TraceRepository traceRepository;
    private final TraceFactory traceFactory;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public UUID logTrace(LogTraceRequest logTraceRequest) {
        // 1. using factory to build a step domain
        Trace trace = traceFactory.createTrace(logTraceRequest);

        // 2. save step
        traceRepository.saveAndFlush(trace);

        // 3. logger

        // 4. return step id
        return trace.getId();
    }
}
