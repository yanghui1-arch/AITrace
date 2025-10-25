package com.supertrace.aitrace.factory;

import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;

public interface TraceFactory {
    Trace createTrace(LogTraceRequest logTraceRequest);
}
