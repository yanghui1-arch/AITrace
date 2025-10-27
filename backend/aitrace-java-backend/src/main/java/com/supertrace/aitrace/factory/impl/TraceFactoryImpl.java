package com.supertrace.aitrace.factory.impl;

import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import com.supertrace.aitrace.factory.TraceFactory;
import org.springframework.stereotype.Component;

import java.util.UUID;

@Component
public class TraceFactoryImpl implements TraceFactory {
    @Override
    public Trace createTrace(LogTraceRequest logTraceRequest) {
        return Trace.builder()
                .id(UUID.fromString(logTraceRequest.getTraceId()))
                .projectName(logTraceRequest.getProjectName())
                .name(logTraceRequest.getTraceName())
                .conversationId(UUID.fromString(logTraceRequest.getConversationId()))
                .tags(logTraceRequest.getTags())
                .input(logTraceRequest.getInput())
                .output(logTraceRequest.getOutput())
                .tracks(logTraceRequest.getTracks())
                .errorInfo(logTraceRequest.getErrorInfo())
                .model(logTraceRequest.getModel())
                .startTime(logTraceRequest.getStartTime())
                .lastUpdateTimestamp(logTraceRequest.getLastUpdateTimestamp())
                .build();
    }
}
