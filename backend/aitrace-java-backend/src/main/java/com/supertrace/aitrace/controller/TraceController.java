package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.LogTraceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

@RestController
@RequestMapping("/api/v0")
public class TraceController {
    private final LogTraceService logTraceService;

    @Autowired
    public TraceController(LogTraceService logTraceService) {
        this.logTraceService = logTraceService;
    }

    @PostMapping("/log/trace")
    public ResponseEntity<APIResponse<UUID>> createAndLogStep(@RequestBody LogTraceRequest logTraceRequest) {
        try {
            System.out.println(logTraceRequest);
            UUID traceId = this.logTraceService.logTrace(logTraceRequest);
            return ResponseEntity.ok(APIResponse.success(traceId));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
