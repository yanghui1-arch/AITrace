package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.TraceService;
import com.supertrace.aitrace.vo.trace.GetTraceVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v0")
public class TraceController {
    private final TraceService traceService;

    @Autowired
    public TraceController(TraceService traceService) {
        this.traceService = traceService;
    }

    @PostMapping("/log/trace")
    public ResponseEntity<APIResponse<UUID>> createAndLogStep(@RequestBody LogTraceRequest logTraceRequest) {
        try {
            System.out.println(logTraceRequest);
            UUID traceId = this.traceService.logTrace(logTraceRequest);
            return ResponseEntity.ok(APIResponse.success(traceId));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/trace/{projectName}")
    public ResponseEntity<APIResponse<List<GetTraceVO>>> getTrace(@PathVariable("projectName") String projectName) {
        try {
            List<Trace> traces = this.traceService.getTrace(projectName);
            List<GetTraceVO> getTraceVOList = new ArrayList<>();
            for (Trace trace : traces) {
                getTraceVOList.add(
                        GetTraceVO.builder()
                                .id(trace.getId())
                                .name(trace.getName())
                                .tags(trace.getTags())
                                .input(trace.getInput())
                                .output(trace.getOutput())
                                .tracks(trace.getTracks())
                                .errorInfo(trace.getErrorInfo())
                                .startTime(trace.getStartTime())
                                .lastUpdateTimestamp(trace.getLastUpdateTimestamp())
                                .build()
                );
            }
            return ResponseEntity.ok(APIResponse.success(getTraceVOList));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(APIResponse.error(e.getMessage()));
        }
    }
}
