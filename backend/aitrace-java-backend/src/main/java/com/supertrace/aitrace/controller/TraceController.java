package com.supertrace.aitrace.controller;

import com.supertrace.aitrace.domain.core.Trace;
import com.supertrace.aitrace.dto.trace.LogTraceRequest;
import com.supertrace.aitrace.exception.AuthenticationException;
import com.supertrace.aitrace.exception.UserIdNotFoundException;
import com.supertrace.aitrace.response.APIResponse;
import com.supertrace.aitrace.service.application.ApiKeyService;
import com.supertrace.aitrace.service.application.LogService;
import com.supertrace.aitrace.service.domain.TraceService;
import com.supertrace.aitrace.utils.ApiKeyUtils;
import com.supertrace.aitrace.vo.trace.GetTraceVO;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v0")
public class TraceController {
    private final TraceService traceService;
    private final ApiKeyService apiKeyService;
    private final LogService logService;

    @PostMapping("/log/trace")
    public ResponseEntity<APIResponse<UUID>> createAndLogStep(
        @RequestHeader(value = "Authorization") String authorization,
        @RequestBody LogTraceRequest logTraceRequest
    ) {
        try {
            String apikey = ApiKeyUtils.extractApiKeyFromHttpHeader(authorization);
            boolean isExisted = this.apiKeyService.isApiKeyExist(apikey);
            if (!isExisted) {
                throw new AuthenticationException();
            }
            UUID userId = this.apiKeyService.resolveUserIdFromApiKey(apikey)
                .orElseThrow(UserIdNotFoundException::new);
            UUID traceId = this.logService.logTrace(userId, logTraceRequest);
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
